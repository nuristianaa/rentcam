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

  def _check_stock(self, item: Item, qty: int):
    if item.stock_available < qty:
      raise BadRequest400(
        f"Stok '{item.name}' tidak cukup. Tersedia: {item.stock_available}, diminta: {qty}"
      )

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
      # FIX: tambah created_by agar konsisten dengan create di tabel lain
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
      self._check_stock(item, req_item.quantity)

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
    """Kembalikan stok saat order dibatalkan."""
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
      #    (pembuatan fine dilakukan terpisah oleh petugas atau background job)
      late_days = 0
      end_dt    = datetime.datetime.combine(data.end_date, datetime.time.max, tzinfo=datetime.timezone.utc)
      if now > end_dt:
        late_days = (now.date() - data.end_date).days

      # 3. Update status rental → selesai
      data = self.repo.update(
        values={"status": "selesai", "updated_by": self.username},
        data=data
      )

      # 4. Catat history
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
        "petugas_name":  petugas.c.name,
      })
      return self.repo.browse(browse_queries=browse_queries, model=model, query=query)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: str):
    try:
      data             = self.repo.get_id(id=id)
      data.items       = self.rental_item_repo.get_by_rental(rental_id=id)
      data.histories   = self.history_repo.get_by_rental(rental_id=id)
      data.checkpoints = self.checkpoint_repo.get_by_rental(rental_id=id)
      return data
    except Exception as e:
      raise BadRequest400(str(e), e)