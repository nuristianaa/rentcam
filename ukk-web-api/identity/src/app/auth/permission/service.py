

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.repo.queries import BrowseSchema
from utils.responses import BadRequest400
from utils.std_service import StdService

from .models import Permission as Model
from .models import Req, tbl_select
from .repo import PermissionRepo


class PermissionService(StdService):
  def __init__(self, db: Session, cred: dict|None) -> None:
    self.repo = PermissionRepo(db=db)
    super().__init__(db, cred, self.repo)

  def store(self, req: Req, id: str|int|None = None):
    # 1. Getting data first
    if id:
      data = self.repo.get_id(id=id)
      before = jsonable_encoder(data)
    values = req.model_dump(exclude_unset=True)
    # 2. Validation if needed
    #
    # 3. Execute
    try:
      if id:
        log_type = 'update'
        values['updated_by'] = self.username
        data = self.repo.update(values=values, data=data)
        log_name = f"{data.get('app')} {data.get('name')}"
        data_log = define_datalog(name=log_name, before=before, after=data)
      else:
        log_type = 'create'
        values['created_by'] = self.username
        data = self.repo.create(values=values)
        log_name = f"{data.get('app')} {data.get('name')}"
        data_log = define_datalog(name=log_name, after=data)
      logs(type=log_type, model=Model, cred=self.cred, data=data_log)
      return data
    except Exception as e:
      raise BadRequest400(str(e), e)

  def bulk_store(self, req: list[Req]):
    failed, updates, inserts = [], [], []
    update_logs, insert_logs = [], []
    existing_map = self.repo.bulk_prepare(req=req)

    # 1. Prepare Values
    for v in req:
      values = v.model_dump()
      try:
        key = (v.app, v.name)
        if key in existing_map:  # update
          r_data = existing_map[key] # type: ignore
          existing = jsonable_encoder(r_data)
          values['id'] = existing.get('id')
          values['updated_by'] = self.username
          values['deleted_at'] = None
          updates.append(values)
          update_logs.append(define_datalog(name=f"{v.app} {v.name}", before=existing, after=values))
        else:  # insert
          values['created_by'] = self.username
          inserts.append(values)
          insert_logs.append(define_datalog(name=f"{v.app} {v.name}", after=values))
      except Exception as e:
        values['msg'] = str(e)
        failed.append(values)

    # 2. Execute Logs
    if inserts and len(inserts) > 0:
      self.repo.bulk_store(values=inserts, action='insert')
      logs(type='create', model=Model, cred=self.cred, data=insert_logs)
    if updates and len(updates) > 0:
      self.repo.bulk_store(values=updates, action='update')
      logs(type='update', model=Model, cred=self.cred, data=update_logs)

    return {
      'success': f'{len(inserts)} data inserted & {len(updates)} data updated',
      'failed': failed
    }

  def get_index(self, browse_queries: BrowseSchema):
    """Returns list based on query."""
    try:
      return self.repo.browse(browse_queries=browse_queries, model=tbl_select())
    except Exception as e:
      raise BadRequest400(str(e), e) from e
