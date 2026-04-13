from typing import Any

from app.auth.permission.models import Permission
from app.auth.user.models import User
from app.auth.user_role.models import UserRole
from sqlalchemy import bindparam, delete, insert, select, text, tuple_, update
from sqlalchemy.orm import Session
from utils.repo.queries import BrowseSchema
from utils.repo.std_repo import StdRepo
from utils.responses import BadRequest400

from .models import PermissionReq, Req, RolePermission
from .models import Role as Model


class RoleRepo(StdRepo):
  def __init__(self, db: Session):
    super().__init__(db, Model)


  def update_permissions(self, req: Req, data: dict):
    try:
      self.db.query(RolePermission).filter(RolePermission.role_id == data['id']).delete()
      inserts = []
      if req.permissions is None: return {}

      for perm in req.permissions:
        permission_id = perm.id
        detail = perm.detail or {}
        row = {
          'role_id': data['id'],
          'permission_id': permission_id,
          'browse': detail.get("browse", False),
          'read': detail.get("read", False),
          'create': detail.get("create", False),
          'update': detail.get("update", False),
          'delete': detail.get("delete", False),
          'restore': detail.get("restore", False),
          'others': detail.get("others", None) or [],
        }
        inserts.append(row)
      if len(inserts) > 0:
        self.db.execute(insert(RolePermission).values(inserts))
      return inserts
    except Exception as e:
      raise BadRequest400(str(e), e)


  def before_delete(self, ids: list[str|int|None]):
    user_ids = (
      self.db.query(UserRole.user_id)
      .join(User, User.id == UserRole.user_id)
      .filter(UserRole.role_id.in_(ids))
      .filter(User.deleted_at.is_(None))
      .count()
    )
    if user_ids > 0:
      msg = f"Deletion Failed. {user_ids} users are still assigned to the selected roles."
      raise BadRequest400(msg)
    return True


  def get_index_and_preview(self, data: Any, browse_queries: BrowseSchema):
    if browse_queries.table:
      raw: list[dict] = data["items"]  # type: ignore
    else:
      raw: list[dict] = data  # type: ignore
    items = []
    for v in raw:
      v: dict
      preview = ""
      try:
        role_id = v["id"]
        query_perm = """
          select
            sum(case when p.app = 'identity' then 1 else 0 end) as app_identity,
            sum(case when p.app = 'crm' then 1 else 0 end) as app_crm,
            sum(case when p.app = 'engineering' then 1 else 0 end) as app_engineering,
            sum(case when p.app = 'finance' then 1 else 0 end) as app_finance,
            sum(case when p.app = 'procurement' then 1 else 0 end) as app_procurement,
            sum(case when p.app = 'project_management' then 1 else 0 end) as app_project_management,
            sum(case when p.app = 'hris' then 1 else 0 end) as app_hris,
            sum(case when p.app = 'rental' then 1 else 0 end) as app_rental
          from auth.roles_permissions rp
          left join auth.permissions p on p.id = rp.permission_id
          where rp.role_id = :role_id
        """
        ex = self.db.execute(text(query_perm), {"role_id": role_id}).first()
        if ex:
          identity         = ex.app_identity
          crm              = ex.app_crm
          engineering      = ex.app_engineering
          finance          = ex.app_finance
          procurement      = ex.app_procurement
          project_management = ex.app_project_management
          hris             = ex.app_hris
          rental           = ex.app_rental
          preview = (
            f"identity: {identity}, crm: {crm}, engineering: {engineering}, "
            f"finance: {finance}, procurement: {procurement}, "
            f"project_management: {project_management}, hris: {hris}, rental: {rental}"
          )
      except Exception as e:
        print(e)
      row = {"id": v["id"], "name": v["name"], "preview": preview}
      items.append(row)
    if browse_queries.table:
      return {"total": data["total"], "items": items}  # type: ignore

    return items


  def get_permissions(self, role_ids: int|list[int]):
    try:
      if isinstance(role_ids, int):
        role_ids = [role_ids]

      query = """
        SELECT
          p.id,
          p.app,
          p.name,
          bool_or(rp.browse) AS browse,
          bool_or(rp.read) AS read,
          bool_or(rp.create) AS create,
          bool_or(rp.update) AS update,
          bool_or(rp.delete) AS delete,
          bool_or(rp.restore) AS restore,
          COALESCE(string_agg(DISTINCT o, ','), '') AS others
        FROM auth.roles_permissions rp
        LEFT JOIN auth.permissions p ON p.id = rp.permission_id
        LEFT JOIN LATERAL jsonb_array_elements_text(COALESCE(rp.others::jsonb, '[]'::jsonb)) AS o ON true
        WHERE rp.role_id = ANY(:role_ids)
        GROUP BY p.id, p.app, p.name;
      """
      result = self.db.execute(text(query), {"role_ids": role_ids}).all()
      return self.format_permissions(result)
    except Exception as e:
      raise BadRequest400(str(e), e)


  def format_permissions(self, result: Any) -> list[dict]:
    permissions = []
    for v in result:
      permissions.append(
        {
          "id": v.id,
          "app": v.app,
          "name": v.name,
          "detail": {
            "browse": v.browse,
            "read": v.read,
            "create": v.create,
            "update": v.update,
            "delete": v.delete,
            "restore": v.restore,
            "others": v.others.split(',') if v.others else None
          },
        }
      )
    return permissions


  def _get_existing_roles(self, role_names: Any):
    roles = (
      self.db.execute(select(Model.id, Model.name).where(Model.name.in_(role_names)).where(Model.deleted_at.is_(None)))
      .mappings()
      .all()
    )
    return {role.get("name"): role for role in roles}


  def _get_indexed_permissions(self, req_permissions: list[PermissionReq]):
    permissions_filter_map = [(item.app, item.permission) for item in req_permissions if item.app and item.permission]

    permissions = (
      self.db.execute(
        select(Permission.id, Permission.app, Permission.name).where(
          tuple_(Permission.app, Permission.name).in_(permissions_filter_map)
        )
      )
      .mappings()
      .all()
    )

    db_permissions = {(p.get("app"), p.get("name")): p for p in permissions if p.get("name")}

    indexed_permissions = []
    for req_perm in req_permissions:
      key = (req_perm.app, req_perm.permission)
      db_perm = db_permissions.get(key)
      if db_perm:
        indexed_permissions.append(
          {
            "id": db_perm["id"],
            "app": req_perm.app,
            "name": db_perm["name"],
            "permission": req_perm.permission,
            "no": req_perm.no,
          }
        )
      else:
        indexed_permissions.append(
          {
            "id": None,
            "app": req_perm.app,
            "name": req_perm.permission,
            "permission": req_perm.permission,
            "no": req_perm.no,
          }
        )
    return indexed_permissions


  def _exec_bulk_upsert(self, updates, inserts):
    if len(updates) > 0:
      stmt = (
        update(Model)
        .where(Model.id == bindparam("b_id"))
        .values(name=bindparam("name"))
        .execution_options(synchronize_session=None)
      )
      self.db.execute(stmt, updates)

    newly_inserted_models = []
    if len(inserts) > 0:
      stmt = insert(Model).values(inserts).returning(Model.id, Model.name)
      result = self.db.execute(stmt)
      newly_inserted_models = result.mappings().all()

    self.db.flush()

    all_data = newly_inserted_models + updates  # type: ignore

    role_name_by_ids = {role.get("name"): role.get("id") for role in all_data}

    role_permissions = []
    for rp in role_permissions:
      if rp["role_id"] is None:
        rp["role_id"] = role_name_by_ids.get(rp.get("role_name"))
      rp.pop("role_name", None)

    if role_permissions:
      role_ids = [role.get("id") for role in all_data]
      self.db.execute(delete(RolePermission).where(RolePermission.role_id.in_(role_ids)))
      stmt = insert(RolePermission).values(role_permissions)
      self.db.execute(stmt)

    return all_data