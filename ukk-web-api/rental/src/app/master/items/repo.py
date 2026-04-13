from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo

from .models import Item as Model


class ItemRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)

  def get_by_code(self, code: str, exclude_id: int | None = None):
    q = self.db.query(Model).filter(
      Model.code == code,
      Model.deleted_at.is_(None)
    )
    if exclude_id:
      q = q.filter(Model.id != exclude_id)
    return q.first()

  def update_stock(self, id: int, stock_available: int, updated_by: str | None = None):
    """Update stock_available — dipanggil saat order dibuat/selesai."""
    obj = self.db.query(Model).filter(Model.id == id).first()
    if obj:
      obj.stock_available = stock_available
      obj.updated_by = updated_by
      self.db.add(obj)
    return obj