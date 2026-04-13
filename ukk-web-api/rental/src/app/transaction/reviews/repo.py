from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo

from .models import Review as Model


class ReviewRepo(StdRepo):
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

  def get_by_item(self, item_id: int) -> list:
    return (
      self.db.query(Model)
      .filter(
        Model.item_id == item_id,
        Model.is_visible == True,
        Model.deleted_at.is_(None)
      )
      .order_by(Model.created_at.desc())
      .all()
    )

  def already_reviewed(self, rental_id: str, item_id: int, customer_id: int) -> bool:
    return (
      self.db.query(Model)
      .filter(
        Model.rental_id == rental_id,
        Model.item_id == item_id,
        Model.customer_id == customer_id,
        Model.deleted_at.is_(None)
      )
      .first()
    ) is not None