
from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.repo.queries import BrowseSchema, BulkId
from utils.responses import BadRequest400

from .models import InsertReqBulk, Req, tbl_select
from .models import Role as Model
from .repo import RoleRepo


class RoleService:
  def __init__(self, db: Session, cred: dict|None) -> None:
    self.repo = RoleRepo(db=db)
    self.cred = cred
    self.username = cred.get('username', None) if cred else None

  def store(self, req: Req, id: str|int|None = None):
    # 1. Getting data first
    if id:
      data = self.repo.get_id(id=id)
      before = jsonable_encoder(data)
    # 2. Model Dump & req validation if needed
    values = req.model_dump(exclude_unset=True, exclude={'permissions'})
    # 3. Execute
    try:
      if id:
        log_type = 'update'
        values['updated_by'] = self.username
        data = self.repo.update(values=values, data=data)
        log_name = data.get('name') # define log name here
        data_log = define_datalog(name=log_name, before=before, after=data)
      else:
        log_type = 'create'
        values['created_by'] = self.username
        data = self.repo.create(values=values)
        log_name = data.get('name') # define log name here
        data_log = define_datalog(name=log_name, after=data)
      data['permissions'] = self.repo.update_permissions(req=req, data=data)
      logs(type=log_type, model=Model, cred=self.cred, data=data_log)
      return data
    except Exception as e:
      raise BadRequest400(str(e), e)

  def get_index(self, browse_queries: BrowseSchema):
    """Returns list based on query."""
    try:
      data = self.repo.browse(browse_queries=browse_queries, model=tbl_select())
      return self.repo.get_index_and_preview(data=data, browse_queries=browse_queries)
    except Exception as e:
      raise BadRequest400(str(e), e) from e

  def get_id(self, id: int):
    """Returns data based on data id."""
    data = self.repo.get_id(id)
    data.permissions = self.repo.get_permissions(data.id)
    return data

  def delete(self, req: BulkId, id: int | None):
    ids: Any = req.id or [id]
    self.repo.before_delete(ids=ids)
    return self.repo.soft_delete(ids=ids, cred=self.cred, action='delete')

  def restore(self, req: BulkId, id: int | None):
    ids: Any = req.id or [id]
    return self.repo.soft_delete(ids=ids, cred=self.cred, action='restore')

  def bulk_insert_or_update(self, req: InsertReqBulk):
    """Bulk insert or update data"""
    if not req.bulk:
      raise BadRequest400("Bulk operation is not enabled")

    try:
      inserts, updates, failed = [], [], []
      exclude_values = {"permissions", "browse", "read", "create", "update", "delete", "restore"}

      indexed_permissions = self.repo._get_indexed_permissions(req_permissions=req.permissions or [])

      role_names = {item.name for item in req.roles if item.name}
      existing_roles = self.repo._get_existing_roles(role_names)

      role_permissions = []

      for item in req.roles:
        try:
          key = item.name
          data = existing_roles.get(key)
          permission_nos = self._expand_permissions(item.permissions)

          if permission_nos == [0]:
            # take all permissions
            filtered_permissions = [p for p in indexed_permissions if p["id"] is not None]
          else:
            # filter normally
            filtered_permissions = [p for p in indexed_permissions if p["no"] in permission_nos and p["id"] is not None]

          role_id = None

          if data:
            role_id = data.id
            values: dict = item.model_dump(exclude_unset=True, exclude=exclude_values)
            values["id"] = data.id
            values["b_id"] = data.id
            values["updated_by"] = self.username
            updates.append(values)
          else:
            values: dict = item.model_dump(exclude_unset=True, exclude=exclude_values)
            values["created_by"] = self.username
            inserts.append(values)

          builded_permissions = self._build_permisisions(filtered_permissions, item)
          for data in builded_permissions:
            role_permissions.append(
              {
                "role_id": role_id,  # assign later if it's new
                "role_name": item.name,
                "permission_id": data["id"],
                "browse": data["detail"]["browse"],
                "read": data["detail"]["read"],
                "create": data["detail"]["create"],
                "update": data["detail"]["update"],
                "delete": data["detail"]["delete"],
                "restore": data["detail"]["restore"],
              }
            )
        except Exception as e:
          failed.append({**item.dict(), "msg": str(e)})

      all_data = self.repo._exec_bulk_upsert(updates, inserts)

      logs(type="create", model=Model, cred=self.cred, data=all_data)

      return {
        "success": f"{len(inserts)} items inserted, {len(updates)} items updated",
        "failed": failed,
      }
    except Exception as e:
      raise BadRequest400(str(e), e)


  def _expand_permissions(self, raw: str | None) -> list[int]:
    result = []

    if not raw: return result
    elif raw == "all": return [0]

    parts = [p.strip() for p in raw.split(",") if p.strip()]

    for part in parts:
      if "-" in part:  # handle ranges like 1-20
        start, end = map(int, part.split("-"))
        result.extend(range(start, end + 1))
      else:  # single number
        result.append(int(part))

    return result


  def _build_permisisions(self, permissions: list, item: Any):
    return [
      {
        "id": permission.get("id"),
        "app": permission.get("app"),
        "name": permission.get("name"),
        "detail": {
          "browse": item.browse or False,
          "read": item.read or False,
          "create": item.create or False,
          "update": item.update or False,
          "delete": item.delete or False,
          "restore": item.restore or False,
        },
      }
      for permission in permissions
    ]
