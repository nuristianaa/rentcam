import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.repo.queries import BrowseSchema
from utils.responses import BadRequest400
from utils.std_service import StdService

from app.transaction.rentals.models import Rental
from app.transaction.rentals.repo import RentalRepo

from .models import Payment as Model
from .models import Req, ReqVerify, tbl_select
from .repo import PaymentRepo

VALID_TYPES    = ['pembayaran', 'denda', 'refund_deposit']
VALID_STATUSES = ['menunggu', 'terverifikasi', 'ditolak']

# Mapping: tipe_payment → status rental yang harus dicapai setelah terverifikasi
PAYMENT_RENTAL_STATUS_MAP = {
  'pembayaran':      'menunggu_verif',
  'denda':           None,
  'refund_deposit':  None,
}


class PaymentService(StdService):
  def __init__(self, db: Session, cred: dict | None) -> None:
    self.repo = PaymentRepo(db=db)
    self.rental_repo = RentalRepo(db=db)
    super().__init__(db, cred, self.repo)

  # ─────────────────────────────────────────────────────────────
  # PRIVATE HELPERS
  # ─────────────────────────────────────────────────────────────

  def _get_payment_attr(self, data, key):
    return data.get(key) if isinstance(data, dict) else getattr(data, key, None)

  def _generate_invoice(self, payment_data, rental) -> None:
    """
    Auto-generate invoice ketika payment berstatus terverifikasi.
    Mendukung multiple invoice — mengizinkan generate ulang untuk payment baru (denda, dsb).
    """
    try:
      from app.transaction.invoice.service import RentalInvoiceService

      payment_id = self._get_payment_attr(payment_data, 'id')
      if not payment_id:
        print("[WARNING] _generate_invoice: payment_id tidak ditemukan, skip.")
        return

      RentalInvoiceService(db=self.db, cred=self.cred).create_from_payment(
        payment_id=str(payment_id)
      )
    except BadRequest400 as e:
      # Duplikat invoice untuk payment YANG SAMA → lewati (idempotent)
      if "sudah ada" in str(e):
        return
      print(f"[WARNING] Invoice generation failed: {e}")
    except Exception as e:
      print(f"[WARNING] Invoice generation failed for payment: {e}")

  def _sync_fine_from_payment(self, payment_data) -> None:
    """
    Jika payment bertipe 'denda' dan terverifikasi, buat entri ke tabel fines
    agar data denda terpusat dan bisa masuk ke laporan.
    """
    try:
      from app.transaction.fines.models import Fine
      payment_id  = self._get_payment_attr(payment_data, 'id')
      rental_id   = self._get_payment_attr(payment_data, 'rental_id')
      amount      = self._get_payment_attr(payment_data, 'amount')
      notes       = self._get_payment_attr(payment_data, 'notes')

      # Cek duplikat berdasarkan description yang memuat payment_id
      existing = self.db.query(Fine).filter(
        Fine.rental_id  == rental_id,
        Fine.description.contains(str(payment_id)),
        Fine.deleted_at.is_(None),
      ).first()
      if existing:
        return  # sudah ada, skip

      fine = Fine(
        rental_id       = rental_id,
        type            = 'denda_pembayaran',
        amount          = amount or 0,
        description     = f"[payment:{payment_id}] {notes or 'Pembayaran denda terverifikasi'}",
        is_paid         = True,
        created_by      = self.username,
      )
      self.db.add(fine)
      self.db.commit()
    except Exception as e:
      print(f"[WARNING] _sync_fine_from_payment failed: {e}")

  def _sync_rental_status(self, payment_data, rental) -> None:
    """
    Sinkronkan status rental setelah payment terverifikasi.
    Hanya payment bertipe 'pembayaran' yang menggerakkan status rental.
    """
    payment_type  = self._get_payment_attr(payment_data, 'type')
    target_status = PAYMENT_RENTAL_STATUS_MAP.get(payment_type)

    if not target_status:
      return  # denda / refund_deposit tidak mengubah status rental

    STATUS_ORDER = [
      'menunggu_bayar', 'menunggu_verif', 'diproses', 'aktif', 'selesai', 'dibatalkan'
    ]
    current_idx = STATUS_ORDER.index(rental.status) if rental.status in STATUS_ORDER else -1
    target_idx  = STATUS_ORDER.index(target_status) if target_status in STATUS_ORDER else -1

    if target_idx > current_idx:
      self.rental_repo.update(
        values={"status": target_status, "updated_by": self.username},
        data=rental
      )

  # ─────────────────────────────────────────────────────────────
  # PUBLIC METHODS
  # ─────────────────────────────────────────────────────────────

  def store(self, req: Req):
    """Customer / admin mencatat pembayaran baru."""

    # 1. Validasi rental
    rental = self.rental_repo.get_id(id=req.rental_id)

    # 2. Validasi tipe
    if req.type not in VALID_TYPES:
      raise BadRequest400(f"Tipe tidak valid. Pilihan: {', '.join(VALID_TYPES)}")

    # 3. Blokir jika masih ada payment 'menunggu' (hanya untuk tipe 'pembayaran')
    if req.type == 'pembayaran':
      pending = self.repo.get_pending_by_rental(req.rental_id)
      if pending:
        raise BadRequest400("Masih ada pembayaran yang menunggu verifikasi untuk order ini.")

    try:
      values = req.model_dump(exclude_unset=True)
      status = str(values.get('status') or 'menunggu').lower()
      if status not in VALID_STATUSES:
        status = 'menunggu'

      values['status']     = status
      values['created_by'] = self.username
      if not values.get('paid_at'):
        values['paid_at'] = datetime.datetime.now()

      # Jika langsung terverifikasi (misal: COD oleh admin), isi verified_by & verified_at
      if status == 'terverifikasi':
        values['verified_by'] = self.user_id
        values['verified_at'] = datetime.datetime.now()

      data = self.repo.create(values=values)
      logs(
        type='create', model=Model, cred=self.cred,
        data=define_datalog(name=f"Payment {rental.rental_code}", after=data),
        schema='transaction'
      )

      # Jika langsung terverifikasi: sync rental status + fine + invoice
      if status == 'terverifikasi':
        rental = self.rental_repo.get_id(id=req.rental_id)
        payment_type = self._get_payment_attr(data, 'type')
        self._sync_rental_status(data, rental)
        # Jika tipe denda: masukkan ke tabel fines dan generate invoice baru
        if payment_type == 'denda':
          self._sync_fine_from_payment(data)
          self._generate_invoice(data, rental)
        elif payment_type == 'pembayaran':
          self._generate_invoice(data, rental)

      # COD menunggu_bayar → langsung ke menunggu_verif
      elif rental.payment_method == 'cod' and rental.status == 'menunggu_bayar':
        self.rental_repo.update(
          values={"status": "menunggu_verif", "updated_by": self.username},
          data=rental
        )

      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  def verify(self, id: str, req: ReqVerify):
    """Petugas verifikasi / tolak bukti pembayaran."""
    data   = self.repo.get_id(id=id)
    before = jsonable_encoder(data)

    if getattr(data, 'status', None) != 'menunggu':
      raise BadRequest400("Hanya pembayaran berstatus 'menunggu' yang bisa diverifikasi.")
    if req.status not in ['terverifikasi', 'ditolak']:
      raise BadRequest400("Status verifikasi harus 'terverifikasi' atau 'ditolak'.")

    try:
      values = {
        "status"      : req.status,
        "verified_by" : self.user_id,
        "verified_at" : datetime.datetime.now(),
        "notes"       : req.notes,
        "updated_by"  : self.username,
      }
      data = self.repo.update(values=values, data=data)

      logs(
        type='verify', model=Model, cred=self.cred,
        data=define_datalog(name=f"Verify Payment → {req.status}", before=before, after=data),
        schema='transaction'
      )

      # Jika terverifikasi: sync rental status + fine (jika denda) + invoice
      if req.status == 'terverifikasi':
        rental_id    = self._get_payment_attr(data, 'rental_id')
        payment_type = self._get_payment_attr(data, 'type')
        if rental_id:
          rental = self.rental_repo.get_id(id=rental_id)
          self._sync_rental_status(data, rental)
          if payment_type == 'denda':
            self._sync_fine_from_payment(data)
            self._generate_invoice(data, rental)
          elif payment_type == 'pembayaran':
            self._generate_invoice(data, rental)

      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  def get_index(self, browse_queries: BrowseSchema):
    try:
      from app.transaction.rentals.models import Rental as RentalModel
      query = select(Model).join(
        RentalModel, RentalModel.id == Model.rental_id, isouter=True
      )
      model = tbl_select(custom_col={"rental_code": RentalModel.rental_code})
      return self.repo.browse(browse_queries=browse_queries, model=model, query=query)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: str):
    try:
      from app.transaction.rentals.models import Rental as RentalModel

      row = (
        self.db.query(Model, RentalModel.rental_code)
        .outerjoin(RentalModel, RentalModel.id == Model.rental_id)
        .filter(Model.id == id, Model.deleted_at.is_(None))
        .first()
      )
      if not row:
        from utils.responses import NotFound404
        raise NotFound404()

      payment, rental_code = row
      result               = jsonable_encoder(payment)
      result['rental_code'] = rental_code
      return result
    except Exception as e:
      raise BadRequest400(str(e), e)