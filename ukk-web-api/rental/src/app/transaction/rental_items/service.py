from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema
from utils.responses import BadRequest400
from utils.std_service import StdService

from app.master.items.models import Item
from app.transaction.rentals.models import Rental

from .models import RentalItem as Model
from .models import tbl_select
from .repo import RentalItemRepo


class RentalItemService(StdService):
  def __init__(self, db: Session, cred: dict | None) -> None:
    self.repo = RentalItemRepo(db=db)
    super().__init__(db, cred, self.repo)

  def get_index(self, browse_queries: BrowseSchema):
    """Browse semua rental items, include nama alat & rental_code."""
    try:
      query = (
        select(Model)
        .join(Item, Item.id == Model.item_id, isouter=True)
        .join(Rental, Rental.id == Model.rental_id, isouter=True)
      )
      model = tbl_select(custom_col={
        "item_name":   Item.name,
        "item_code":   Item.code,
        "item_brand":  Item.brand,
        "rental_code": Rental.rental_code,
        "rental_status": Rental.status,
      })
      return self.repo.browse(browse_queries=browse_queries, model=model, query=query)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: str):
    try:
      return self.repo.get_id(id=id)
    except Exception as e:
      raise BadRequest400(str(e), e)

  def get_by_rental(self, rental_id: str):
    """Ambil semua item dari 1 rental — include detail alat."""
    try:
      return self.repo.get_by_rental(rental_id=rental_id)
    except Exception as e:
      raise BadRequest400(str(e), e)