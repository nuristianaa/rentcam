from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.repo.queries import BrowseSchema, BulkId
from utils.responses import BadRequest400
from utils.std_service import StdService

from .models import ItemCategory as Model
from .models import Req, tbl_select
from .repo import ItemCategoryRepo


class ItemCategoryService(StdService):
  def __init__(self, db: Session, cred: dict | None) -> None:
    self.repo = ItemCategoryRepo(db=db)
    super().__init__(db, cred, self.repo)

  def store(self, req: Req, id: int | None = None):
    # 1. Getting data first
    if id:
      data = self.repo.get_id(id=id)
      before = jsonable_encoder(data)

    values = req.model_dump(exclude_unset=True)

    # 2. Validation: name harus unik
    q = self.db.query(Model).filter(
      Model.name == values.get('name'),
      Model.deleted_at.is_(None)
    )
    if id:
      q = q.filter(Model.id != id)
    if q.first():
      raise BadRequest400(f"Kategori dengan nama '{values.get('name')}' sudah ada.")

    # 3. Execute
    try:
      if id:
        log_type = 'update'
        values['updated_by'] = self.username
        data = self.repo.update(values=values, data=data)
        log_name = data.get('name')
        data_log = define_datalog(name=log_name, before=before, after=data)
      else:
        log_type = 'create'
        values['created_by'] = self.username
        data = self.repo.create(values=values)
        log_name = data.get('name')
        data_log = define_datalog(name=log_name, after=data)

      logs(type=log_type, model=Model, cred=self.cred, data=data_log, schema='master')
      return data
    except Exception as e:
      raise BadRequest400(str(e), e)

  def get_index(self, browse_queries: BrowseSchema):
    try:
      query = select(Model)
      model = tbl_select()
      return self.repo.browse(browse_queries=browse_queries, model=model, query=query)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: int):
    try:
      return self.repo.get_id(id=id)
    except Exception as e:
      raise BadRequest400(str(e), e)