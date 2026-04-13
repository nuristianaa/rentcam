from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo

from .models import RentalCheckpoint as Model


class RentalCheckpointRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)

  def get_by_rental(self, rental_id: str) -> list[Model]:
    """Ambil semua checkpoint (checkout + checkin) sebuah rental."""
    return (
      self.db.query(Model)
      .filter(
        Model.rental_id == rental_id,
        Model.deleted_at.is_(None),
      )
      .order_by(Model.actual_at.asc())
      .all()
    )

  def get_by_rental_and_type(self, rental_id: str, type: str) -> Model | None:
    """Cek apakah sudah ada checkpoint dengan type tertentu (untuk guard duplikat)."""
    return (
      self.db.query(Model)
      .filter(
        Model.rental_id == rental_id,
        Model.type == type,
        Model.deleted_at.is_(None),
      )
      .first()
    )