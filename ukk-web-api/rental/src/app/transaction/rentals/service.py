import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.repo.queries import BrowseSchema
from utils.responses import BadRequest400
from utils.std_service import StdService

from app.master.items.models import Item
from app.master.items.repo import ItemRepo
from app.transaction.rental_items.models import RentalItem
from app.transaction.rental_items.repo import RentalItemRepo
from app.transaction.rentals_histories.repo import RentalHistoryRepo
from app.transaction.rental_checkpoints.repo import RentalCheckpointRepo
from app.transaction.invoice.repo import RentalInvoiceRepo
from app.transaction.payments.repo import PaymentRepo
from .models import Rental as Model
from .models import Req, ReqCheckpoint, ReqUpdateStatus, tbl_select
from .repo import RentalRepo

# Status yang boleh diubah dan ke mana boleh pindah.
# checkout (diproses → aktif) dan checkin (aktif → selesai) ditangani
# oleh endpoint tersendiri, bukan update_status.
VALID_STATUS_FLOW = {
  "menunggu_bayar": ["menunggu_verif", "dibatalkan"],
  "menunggu_verif": ["diproses", "menunggu_bayar", "dibatalkan"],
  "diproses":       ["dibatalkan"],   # aktif hanya bisa lewat /checkout
  "aktif":          [],               # selesai hanya bisa lewat /checkin
  "selesai":        [],
  "dibatalkan":     [],
}

VALID_PAYMENT_METHODS = ["transfer", "cod"]


class RentalService(StdService):
  def __init__(self, db: Session, cred: dict | None) -> None:
    self.repo             = RentalRepo(db=db)
    self.item_repo        = ItemRepo(db=db)
    self.rental_item_repo = RentalItemRepo(db=db)
    self.history_repo     = RentalHistoryRepo(db=db)
    self.checkpoint_repo  = RentalCheckpointRepo(db=db)
    self.invoice_repo     = RentalInvoiceRepo(db=db)
    self.payment_repo     = PaymentRepo(db=db)
    super().__init__(db, cred, self.repo)

  # ─────────────────────────────────────────
  # HELPERS
  # ─────────────────────────────────────────

  def _validate_payment_method(self, method: str):
    if method not in VALID_PAYMENT_METHODS:
      raise BadRequest400(f"Metode bayar tidak valid. Pilihan: {', '.join(VALID_PAYMENT_METHODS)}")

  def _validate_dates(self, start: datetime.date, end: datetime.date):
    if end <= start:
      raise BadRequest400("Tanggal selesai harus setelah tanggal mulai.")

  def _get_item_or_raise(self, item_id: int) -> Item:
    item = self.db.query(Item).filter(
      Item.id == item_id,
      Item.is_active == True,
      Item.deleted_at.is_(None)
    ).first()
    if not item:
      raise BadRequest400(f"Alat ID {item_id} tidak ditemukan atau tidak aktif.")
    return item

  def _check_stock_for_dates(self, item: Item, qty: int, start_date: datetime.date, end_date: datetime.date):
    reservations = self.repo.get_reserved_quantities_by_item(item.id, start_date, end_date)
    current = start_date
    while current <= end_date:
      reserved = 0
      for r_start, r_end, r_qty in reservations:
        if r_start <= current <= r_end:
          reserved += r_qty
      available = max((item.stock_total or 0) - reserved, 0)
      if available < qty:
        raise BadRequest400(
          f"Stok '{item.name}' tidak cukup untuk tanggal {current.strftime('%Y-%m-%d')}. "
          f"Tersedia: {available}, Diminta: {qty}"
        )
      current += datetime.timedelta(days=1)

  def _record_history(
    self,
    rental_id: str,
    event: str,
    old_status: str | None = None,
    new_status: str | None = None,
    notes: str | None = None,
    data: dict | None = None,
  ):
    """Insert satu baris ke rental_histories."""
    self.history_repo.create(values={
      "rental_id":  rental_id,
      "event":      event,
      "old_status": old_status,
      "new_status": new_status,
      "actor":      self.username,
      "actor_id":   self.cred.get("user_id") if self.cred else None,
      "notes":      notes,
      "data":       data,
      "created_by": self.username,
    })

  # ─────────────────────────────────────────
  # CREATE
  # ─────────────────────────────────────────

  def store(self, req: Req):
    # 1. Validasi
    self._validate_payment_method(req.payment_method)
    self._validate_dates(req.start_date, req.end_date)
    if not req.items:
      raise BadRequest400("Minimal 1 alat harus dipilih.")

    duration = (req.end_date - req.start_date).days

    # 2. Validasi stok & hitung total
    subtotal      = 0.0
    deposit_total = 0.0
    item_rows     = []

    for req_item in req.items:
      item = self._get_item_or_raise(req_item.item_id)
      self._check_stock_for_dates(item, req_item.quantity, req.start_date, req.end_date)

      item_subtotal  = item.price_per_day * req_item.quantity * duration
      subtotal      += item_subtotal
      deposit_total += (item.deposit_amount or 0) * req_item.quantity
      item_rows.append({
        "item":           item,
        "quantity":       req_item.quantity,
        "price_per_day":  item.price_per_day,
        "deposit_amount": item.deposit_amount or 0,
        "subtotal":       item_subtotal,
      })

    grand_total = subtotal + deposit_total

    try:
      # 3. Buat rental
      rental_code   = self.repo.generate_code()
      rental_values = {
        "rental_code":    rental_code,
        "customer_id":    req.customer_id,
        "start_date":     req.start_date,
        "end_date":       req.end_date,
        "duration_days":  duration,
        "subtotal":       subtotal,
        "deposit_total":  deposit_total,
        "grand_total":    grand_total,
        "payment_method": req.payment_method,
        "status":         "menunggu_bayar",
        "notes":          req.notes,
        "created_by":     self.username,
      }
      data = self.repo.create(values=rental_values)

      # 4. Buat rental_items & kurangi stok
      for row in item_rows:
        self.rental_item_repo.create(values={
          "rental_id":      data.get("id"),
          "item_id":        row["item"].id,
          "quantity":       row["quantity"],
          "price_per_day":  row["price_per_day"],
          "deposit_amount": row["deposit_amount"],
          "subtotal":       row["subtotal"],
          "created_by":     self.username,
        })
        new_stock = row["item"].stock_available - row["quantity"]
        self.item_repo.update_stock(row["item"].id, new_stock, self.username)

      logs(
        type="create", model=Model, cred=self.cred,
        data=define_datalog(name=rental_code, after=data),
        schema="transaction"
      )

      # Catat history — status awal
      self._record_history(
        rental_id  = data.get("id"),
        event      = "status_changed",
        old_status = None,
        new_status = "menunggu_bayar",
        notes      = req.notes,
      )

      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  # ─────────────────────────────────────────
  # UPDATE FULL
  # ─────────────────────────────────────────

  def update(self, id: str, req: Req):
    data = self.repo.get_id(id=id)
    before = jsonable_encoder(data)

    if data.status in ["aktif", "selesai", "dibatalkan"]:
      raise BadRequest400(f"Rental dengan status '{data.status}' tidak boleh diubah.")

    self._validate_payment_method(req.payment_method)
    self._validate_dates(req.start_date, req.end_date)
    duration = (req.end_date - req.start_date).days

    if not req.items: raise BadRequest400("Minimal 1 alat harus dipilih.")

    subtotal = 0.0
    deposit_total = 0.0
    item_rows = []

    for req_item in req.items:
      it = self._get_item_or_raise(req_item.item_id)
      it_subtotal  = it.price_per_day * req_item.quantity * duration
      subtotal      += it_subtotal
      deposit_total += (it.deposit_amount or 0) * req_item.quantity
      item_rows.append({
        "item":           it,
        "quantity":       req_item.quantity,
        "price_per_day":  it.price_per_day,
        "deposit_amount": it.deposit_amount or 0,
        "subtotal":       it_subtotal,
      })

    grand_total = subtotal + deposit_total

    try:
      # Restore old stock
      old_items = self.rental_item_repo.get_by_rental(id)
      for old in old_items:
        old_qty = old.get("quantity") if isinstance(old, dict) else getattr(old, "quantity", 0)
        old_item_id = old.get("item_id") if isinstance(old, dict) else getattr(old, "item_id", None)
        it = self.db.query(Item).filter(Item.id == old_item_id).first()
        if it:
          self.item_repo.update_stock(it.id, it.stock_available + old_qty, self.username)

      # Remove old rental_items before re-inserting
      from sqlalchemy import delete
      self.db.execute(delete(RentalItem).where(RentalItem.rental_id == id))
      self.db.flush()

      # Resolve petugas_id: gunakan nilai dari request jika ada, fallback ke nilai di DB
      req_petugas_id = getattr(req, "petugas_id", None)
      resolved_petugas_id = req_petugas_id if req_petugas_id is not None else data.petugas_id

      rental_values = {
        "customer_id":    req.customer_id,
        "petugas_id":     resolved_petugas_id,
        "start_date":     req.start_date,
        "end_date":       req.end_date,
        "duration_days":  duration,
        "subtotal":       subtotal,
        "deposit_total":  deposit_total,
        "grand_total":    grand_total,
        "payment_method": req.payment_method,
        "notes":          req.notes,
        "updated_by":     self.username,
      }

      # Perbolehkan edit status dari UI
      req_status = getattr(req, "status", None)
      if req_status and req_status != data.status:
        rental_values["status"] = req_status

      data = self.repo.update(values=rental_values, data=data)

      # Validate new stock for dates (after old items removed)
      for req_item in req.items:
        it = self._get_item_or_raise(req_item.item_id)
        self._check_stock_for_dates(it, req_item.quantity, req.start_date, req.end_date)

      for row in item_rows:
        self.rental_item_repo.create(values={
          "rental_id":      data.get("id"),
          "item_id":        row["item"].id,
          "quantity":       row["quantity"],
          "price_per_day":  row["price_per_day"],
          "deposit_amount": row["deposit_amount"],
          "subtotal":       row["subtotal"],
          "created_by":     self.username,
        })
        new_stock = row["item"].stock_available - row["quantity"]
        self.item_repo.update_stock(row["item"].id, new_stock, self.username)

      logs(type="update", model=Model, cred=self.cred, data=define_datalog(name=data.get('rental_code'), before=before, after=data), schema="transaction")
      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  # ─────────────────────────────────────────
  # UPDATE STATUS
  # ─────────────────────────────────────────

  def update_status(self, id: str, req: ReqUpdateStatus):
    data    = self.repo.get_id(id=id)
    before  = jsonable_encoder(data)
    current = data.status
    allowed = VALID_STATUS_FLOW.get(current, [])

    if req.status not in allowed:
      raise BadRequest400(
        f"Perubahan status tidak valid: {current} → {req.status}. "
        f"Status yang diperbolehkan: {', '.join(allowed) or '-'}"
      )

    values = {"status": req.status, "updated_by": self.username}
    if req.petugas_id:
      values["petugas_id"] = req.petugas_id
    if req.notes:
      values["notes"] = req.notes

    # Jika dibatalkan, kembalikan stok
    if req.status == "dibatalkan":
      self._restore_stock(id)

    try:
      data = self.repo.update(values=values, data=data)

      self._record_history(
        rental_id  = id,
        event      = "status_changed",
        old_status = current,
        new_status = req.status,
        notes      = req.notes,
        data       = before,
      )

      logs(
        type="update_status", model=Model, cred=self.cred,
        data=define_datalog(
          name=f"{data.get('rental_code')} → {req.status}",
          before=before, after=data
        ),
        schema="transaction"
      )
      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  def _restore_stock(self, rental_id: str):
    """Kembalikan stok saat order dibatalkan atau saat rental selesai tanpa kerusakan."""
    rows = self.db.query(RentalItem).filter(
      RentalItem.rental_id == rental_id,
      RentalItem.deleted_at.is_(None)
    ).all()
    for row in rows:
      item = self.db.query(Item).filter(Item.id == row.item_id).first()
      if item:
        self.item_repo.update_stock(
          item.id,
          item.stock_available + row.quantity,
          self.username
        )

  def _should_restore_stock(self, condition: str | None) -> bool:
    """Determine whether returned rental items should be returned to stock."""
    return condition not in ["rusak", "hilang"]

  # ─────────────────────────────────────────
  # CHECKOUT — diproses → aktif
  # ─────────────────────────────────────────

  def checkout(self, id: str, req: ReqCheckpoint):
    data = self.repo.get_id(id=id)

    if data.status != "diproses":
      raise BadRequest400(
        f"Checkout hanya bisa dilakukan saat status 'diproses'. Status saat ini: '{data.status}'"
      )

    # Cek apakah sudah pernah checkout
    existing = self.checkpoint_repo.get_by_rental_and_type(rental_id=id, type="checkout")
    if existing:
      raise BadRequest400("Rental ini sudah pernah di-checkout.")

    try:
      now = datetime.datetime.now(datetime.timezone.utc)

      # 1. Simpan checkpoint
      self.checkpoint_repo.create(values={
        "rental_id":          id,
        "type":               "checkout",
        "actual_at":          now,
        "condition":          req.condition,
        "condition_notes":    req.condition_notes,
        "checklist":          req.checklist,
        "officer_id":         req.officer_id,
        "officer_name":       self.cred.get("name") if self.cred else None,
        "customer_signature": req.customer_signature,
        "notes":              req.notes,
        "created_by":         self.username,
      })

      # 2. Update status rental → aktif
      data = self.repo.update(
        values={"status": "aktif", "updated_by": self.username},
        data=data
      )

      # 3. Catat history
      self._record_history(
        rental_id  = id,
        event      = "checkout",
        old_status = "diproses",
        new_status = "aktif",
        notes      = req.notes,
        data       = {"actual_checkout_at": now.isoformat()},
      )

      logs(
        type="checkout", model=Model, cred=self.cred,
        data=define_datalog(name=f"{data.get('rental_code')} checkout", after=data),
        schema="transaction"
      )
      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  # ─────────────────────────────────────────
  # CHECKIN — aktif → selesai
  # ─────────────────────────────────────────

  def checkin(self, id: str, req: ReqCheckpoint):
    data = self.repo.get_id(id=id)

    if data.status != "aktif":
      raise BadRequest400(
        f"Checkin hanya bisa dilakukan saat status 'aktif'. Status saat ini: '{data.status}'"
      )

    # Cek apakah sudah pernah checkin
    existing = self.checkpoint_repo.get_by_rental_and_type(rental_id=id, type="checkin")
    if existing:
      raise BadRequest400("Rental ini sudah pernah di-checkin.")

    try:
      now = datetime.datetime.now(datetime.timezone.utc)

      # 1. Simpan checkpoint
      self.checkpoint_repo.create(values={
        "rental_id":          id,
        "type":               "checkin",
        "actual_at":          now,
        "condition":          req.condition,
        "condition_notes":    req.condition_notes,
        "checklist":          req.checklist,
        "officer_id":         req.officer_id,
        "officer_name":       self.cred.get("name") if self.cred else None,
        "customer_signature": req.customer_signature,
        "notes":              req.notes,
        "created_by":         self.username,
      })

      # 2. Cek keterlambatan
      late_days = 0
      end_dt    = datetime.datetime.combine(data.end_date, datetime.time.max, tzinfo=datetime.timezone.utc)
      if now > end_dt:
        late_days = (now.date() - data.end_date).days

      # 3. Update status rental → selesai
      data = self.repo.update(
        values={"status": "selesai", "updated_by": self.username},
        data=data
      )

      # 4. Kembalikan stok jika alat tidak hilang atau rusak berat
      if self._should_restore_stock(req.condition):
        self._restore_stock(id)

      # 5. Catat history
      self._record_history(
        rental_id  = id,
        event      = "checkin",
        old_status = "aktif",
        new_status = "selesai",
        notes      = req.notes,
        data       = {
          "actual_checkin_at": now.isoformat(),
          "condition":         req.condition,
          "late_days":         late_days,
        },
      )

      logs(
        type="checkin", model=Model, cred=self.cred,
        data=define_datalog(name=f"{data.get('rental_code')} checkin", after=data),
        schema="transaction"
      )
      return {**data, "late_days": late_days}
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  # ─────────────────────────────────────────
  # READ
  # ─────────────────────────────────────────

  def get_index(self, browse_queries: BrowseSchema):
    try:
      from app.auth.user.models import User
      customer = User.__table__.alias("customer")
      petugas  = User.__table__.alias("petugas")

      query = (
        select(Model)
        .join(customer, customer.c.id == Model.customer_id, isouter=True)
        .join(petugas,  petugas.c.id  == Model.petugas_id,  isouter=True)
      )
      model = tbl_select(custom_col={
        "customer_name": customer.c.name,
        "customer_email": customer.c.email,
        "petugas_name":  petugas.c.name,
      })
      return self.repo.browse(browse_queries=browse_queries, model=model, query=query)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: str):
    try:
      data = self.repo.get_id(id=id)
      result = jsonable_encoder(data)
      result["customer_name"] = data.customer.name if getattr(data, "customer", None) else None
      result["customer_email"] = data.customer.email if getattr(data, "customer", None) else None
      result["petugas_name"] = data.petugas.name if getattr(data, "petugas", None) else None
      result["items"] = self.rental_item_repo.get_by_rental(rental_id=id)
      result["histories"] = self.history_repo.get_by_rental(rental_id=id)
      result["checkpoints"] = self.checkpoint_repo.get_by_rental(rental_id=id)
      result["invoices"] = self.invoice_repo.get_by_rental(rental_id=id)
      result["payments"] = self.payment_repo.get_by_rental(rental_id=id)

      from app.transaction.reviews.repo import ReviewRepo
      result["reviews"] = ReviewRepo(db=self.db).get_by_rental(rental_id=id)

      return result
    except Exception as e:
      raise BadRequest400(str(e), e)