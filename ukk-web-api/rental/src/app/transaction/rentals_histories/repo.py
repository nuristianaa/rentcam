from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo
from utils.responses import NotFound404

from .models import RentalHistory as Model


class RentalHistoryRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)

  def get_id(self, id: str) -> Model:
    """Ambil satu history berdasarkan ID."""
    row = self.db.query(Model).filter(
      Model.id == id,
      Model.deleted_at.is_(None),
    ).first()
    if not row:
      raise NotFound404()
    return row

  def get_by_rental(self, rental_id: str) -> list[Model]:
    """Ambil semua history sebuah rental, urut dari terlama."""
    return (
      self.db.query(Model)
      .filter(
        Model.rental_id == rental_id,
        Model.deleted_at.is_(None),
      )
      .order_by(Model.created_at.asc())
      .all()
    )

  def get_by_event(self, rental_id: str, event: str) -> list[Model]:
    """Ambil history berdasarkan jenis event tertentu."""
    return (
      self.db.query(Model)
      .filter(
        Model.rental_id == rental_id,
        Model.event == event,
        Model.deleted_at.is_(None),
      )
      .order_by(Model.created_at.asc())
      .all()
    )