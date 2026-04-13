from sqlalchemy.orm import Session
from utils.repo.std_repo import StdRepo

from .models import RentalItem as Model


class RentalItemRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)

  def get_by_rental(self, rental_id: str) -> list:
    """Ambil semua item dari satu rental, include nama alat."""
    from app.master.items.models import Item
    from sqlalchemy import select
    rows = (
      self.db.query(Model, Item.name, Item.code, Item.brand)
      .join(Item, Item.id == Model.item_id, isouter=True)
      .filter(
        Model.rental_id == rental_id,
        Model.deleted_at.is_(None)
      )
      .all()
    )
    result = []
    for row, item_name, item_code, item_brand in rows:
      d = {c.name: getattr(row, c.name) for c in row.__table__.columns}
      d['item_name'] = item_name
      d['item_code'] = item_code
      d['item_brand'] = item_brand
      result.append(d)
    return result