import datetime
from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo
from utils.responses import NotFound404

from .models import RentalInvoice as Model


class RentalInvoiceRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)

  def generate_code(self) -> str:
    """Generate invoice_code format INV-YYYYMMDD-NNN."""
    today  = datetime.date.today().strftime("%Y%m%d")
    prefix = f"INV-{today}-"
    last   = (
      self.db.query(Model)
      .filter(Model.invoice_code.like(f"{prefix}%"))
      .order_by(Model.invoice_code.desc())
      .first()
    )
    seq = int(last.invoice_code.split("-")[-1]) + 1 if last else 1
    return f"{prefix}{seq:03d}"

  def get_id(self, id: str) -> Model:
    row = self.db.query(Model).filter(
      Model.id == id,
      Model.deleted_at.is_(None),
    ).first()
    if not row:
      raise NotFound404()
    return row

  def get_by_payment(self, payment_id: str) -> Model | None:
    """Cek apakah payment sudah punya invoice (untuk guard duplikat)."""
    return self.db.query(Model).filter(
      Model.payment_id == payment_id,
      Model.deleted_at.is_(None),
    ).first()

  def get_by_rental(self, rental_id: str) -> list[Model]:
    """Ambil semua invoice sebuah rental."""
    return (
      self.db.query(Model)
      .filter(
        Model.rental_id == rental_id,
        Model.deleted_at.is_(None),
      )
      .order_by(Model.created_at.asc())
      .all()
    )

  def get_pending_pdf(self) -> list[Model]:
    """Ambil invoice yang PDF-nya belum di-generate — untuk background job."""
    return (
      self.db.query(Model)
      .filter(
        Model.pdf_status == "pending",
        Model.deleted_at.is_(None),
      )
      .order_by(Model.created_at.asc())
      .all()
    )