from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.repo.queries import BrowseSchema
from utils.responses import BadRequest400
from utils.std_service import StdService

from app.transaction.rentals.repo import RentalRepo

from .models import Review as Model
from .models import Req, ReqToggleVisible, tbl_select
from .repo import ReviewRepo


class ReviewService(StdService):
  def __init__(self, db: Session, cred: dict | None) -> None:
    self.repo = ReviewRepo(db=db)
    self.rental_repo = RentalRepo(db=db)
    super().__init__(db, cred, self.repo)

  def store(self, req: Req):
    # 1. Validasi rental ada dan statusnya selesai
    rental = self.rental_repo.get_id(id=req.rental_id)
    if rental.status != 'selesai':
      raise BadRequest400("Review hanya bisa dibuat untuk rental yang sudah selesai.")

    # 2. Validasi customer adalah pemilik rental
    if rental.customer_id != self.user_id:
      raise BadRequest400("Kamu tidak berhak membuat review untuk rental ini.")

    # 3. Cek sudah pernah review item yang sama di rental ini
    if self.repo.already_reviewed(rental_id=req.rental_id, item_id=req.item_id, customer_id=self.user_id):
      raise BadRequest400("Kamu sudah memberikan review untuk alat ini.")

    try:
      values = req.model_dump(exclude_unset=True)
      values['customer_id'] = self.user_id
      values['created_by'] = self.username
      values['is_visible'] = True

      data = self.repo.create(values=values)
      logs(
        type='create', model=Model, cred=self.cred,
        data=define_datalog(
          name=f"Review rental {rental.rental_code}",
          after=data
        ),
        schema='transaction'
      )
      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  def toggle_visible(self, id: str, req: ReqToggleVisible):
    """Admin sembunyikan / tampilkan review."""
    data = self.repo.get_id(id=id)
    before = jsonable_encoder(data)

    try:
      values = {
        "is_visible": req.is_visible,
        "updated_by": self.username,
      }
      data = self.repo.update(values=values, data=data)
      logs(
        type='toggle_visible', model=Model, cred=self.cred,
        data=define_datalog(
          name=f"Review {'ditampilkan' if req.is_visible else 'disembunyikan'}",
          before=before, after=data
        ),
        schema='transaction'
      )
      return data
    except BadRequest400:
      raise
    except Exception as e:
      raise BadRequest400(str(e), e)

  def get_index(self, browse_queries: BrowseSchema):
    try:
      from app.transaction.rentals.models import Rental as RentalModel
      from app.master.items.models import Item as ItemModel
      query = (
        select(Model)
        .join(RentalModel, RentalModel.id == Model.rental_id, isouter=True)
        .join(ItemModel, ItemModel.id == Model.item_id, isouter=True)
      )
      model = tbl_select(custom_col={
        "rental_code": RentalModel.rental_code,
        "item_name": ItemModel.name,
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
    try:
      return self.repo.get_by_rental(rental_id=rental_id)
    except Exception as e:
      raise BadRequest400(str(e), e)

  def get_by_item(self, item_id: int):
    try:
      return self.repo.get_by_item(item_id=item_id)
    except Exception as e:
      raise BadRequest400(str(e), e)