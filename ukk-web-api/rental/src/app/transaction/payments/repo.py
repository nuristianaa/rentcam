from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo

from .models import Payment as Model


class PaymentRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)

  def get_by_rental(self, rental_id: str) -> list:
    return (
      self.db.query(Model)
      .filter(
        Model.rental_id == rental_id,
        Model.deleted_at.is_(None)
      )
      .order_by(Model.created_at.desc())
      .all()
    )

  def get_pending_by_rental(self, rental_id: str):
    """Ambil payment yg belum diverif untuk 1 rental."""
    return (
      self.db.query(Model)
      .filter(
        Model.rental_id == rental_id,
        Model.status == 'menunggu',
        Model.deleted_at.is_(None)
      )
      .first()
    )