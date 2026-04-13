import datetime
from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo
from utils.responses import NotFound404

from .models import Rental as Model


class RentalRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)

  def generate_code(self) -> str:
    """Generate rental_code format RF-YYYYMMDD-NNN."""
    today = datetime.date.today().strftime("%Y%m%d")
    prefix = f"RF-{today}-"
    last = (
      self.db.query(Model)
      .filter(Model.rental_code.like(f"{prefix}%"))
      .order_by(Model.rental_code.desc())
      .first()
    )
    if last:
      seq = int(last.rental_code.split("-")[-1]) + 1
    else:
      seq = 1
    return f"{prefix}{seq:03d}"

  def get_id(self, id: str) -> Model:
    row = self.db.query(Model).filter(
      Model.id == id,
      Model.deleted_at.is_(None)
    ).first()
    if not row:
      raise NotFound404()
    return row

  def get_active_by_item(self, item_id: int) -> list:
    """Ambil rental aktif yang mengandung item tertentu — untuk cek stok."""
    from app.transaction.rental_items.models import RentalItem
    return (
      self.db.query(Model)
      .join(RentalItem, RentalItem.rental_id == Model.id)
      .filter(
        RentalItem.item_id == item_id,
        Model.status.in_(["diproses", "aktif"]),
        Model.deleted_at.is_(None)
      )
      .all()
    )

  def get_reserved_quantities_by_item(self, item_id: int, start_date: datetime.date, end_date: datetime.date) -> list:
    """Ambil jumlah reserved per tanggal untuk item tertentu."""
    from app.transaction.rental_items.models import RentalItem
    return (
      self.db.query(Model.start_date, Model.end_date, RentalItem.quantity)
      .join(RentalItem, RentalItem.rental_id == Model.id)
      .filter(
        RentalItem.item_id == item_id,
        Model.status.in_(['menunggu_bayar', 'menunggu_verif', 'diproses', 'aktif']),
        Model.deleted_at.is_(None),
        Model.start_date <= end_date,
        Model.end_date >= start_date,
      )
      .all()
    )