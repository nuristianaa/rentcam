import requests
from app.auth.notification.models import Notification
from app.auth.oauth2 import create_jwt_full
from app.auth.role.models import Role
from app.auth.role.repo import RoleRepo
from app.auth.user_role.models import UserRole
from config import getenv
from sqlalchemy import func, select
from sqlalchemy.orm import Mapped, Session, joinedload
from utils.repo.queries import BrowseSchema, BulkId, browse, soft_delete
from utils.responses import BadRequest400, NotFound404

from ..models import User as Model
from ..schema import FavMenu

module_name = "User"


def get_index(db: Session, browse_queries: BrowseSchema):
  try:
    subquery_roles = (
      select(func.string_agg(Role.name, ", "))
      .select_from(UserRole)
      .join(Role, UserRole.role_id == Role.id)
      .where(UserRole.user_id == Model.id)
      .correlate(Model)
      .scalar_subquery()
    )

    model: dict[str, Mapped] = {
      "id"                    : Model.id,
      "name"                  : Model.name,
      "username"              : Model.username,
      "email"                 : Model.email,
      "phone"                 : Model.phone,
      "title"                 : Model.title,
      "is_active"             : Model.is_active,
      "role_names"            : subquery_roles.label("role_names"),  # type: ignore
      "notifications"         : Model.notifications,
      "additional_permissions": Model.additional_permissions,
      "location"              : Model.location,
      "country_code"          : Model.country_code,
      "birthday"              : Model.birthday,
      "created_by"            : Model.created_by,
      "updated_by"            : Model.updated_by,
      "deleted_by"            : Model.deleted_by,
      "created_at"            : Model.created_at,
      "updated_at"            : Model.updated_at,
      "deleted_at"            : Model.deleted_at,
    }
    query = (
      select()
    )
    return browse(browse_queries=browse_queries, model=model, query=query, db=db)
  except Exception as e:
    raise BadRequest400(str(e), e)


def get_users_by_role(role_id, db, browse_queries: BrowseSchema):
  try:
    model: dict[str, Mapped] = {
      "name"    : Model.name,
      "username": Model.username,
    }
    query = (
      select()
      .join(UserRole, UserRole.user_id == Model.id, isouter=False)
      .where(UserRole.role_id == role_id)
    )
    return browse(browse_queries=browse_queries, model=model, query=query, db=db)
  except Exception as e:
    raise BadRequest400(str(e), e)


def get_id(id: int, db: Session) -> Model | None:
  try:
    return (
      db.query(Model)
      .options(joinedload(Model.roles))
      .filter(Model.id == id, Model.deleted_at.is_(None))
      .first()
    )
  except Exception as e:
    raise BadRequest400(str(e), e)


def get_by_cred(cred: dict, db: Session, refresh_token: int | None = 0) -> Model:
  try:
    username = cred.get("username")
    model = (
      db.query(Model)
      .options(joinedload(Model.roles))
      .filter(Model.username == username)
      .first()
    )

    if not model:
      raise NotFound404(message=f"Data {Model.__tablename__} not Found")

    role_codes = db.execute(
      select(Role.name)
      .join(UserRole, Role.id == UserRole.role_id)
      .filter(UserRole.user_id == model.id)
    ).scalars().all()

    role_codes_str = ",".join(role_codes) if role_codes else ""

    if refresh_token == 1 or refresh_token == 2:
      expiry = int(getenv("JWT_EXPIRED_MINUTE", "30"))
      if refresh_token == 2:
        expiry = int(getenv("JWT_EXPIRED_REMEMBER", "1440"))
      data = create_jwt_full(user=model, expiry=expiry, role_codes=role_codes_str)
      model.access_token = data["access_token"]
      model.refresh_token = data["refresh_token"]
      model.expire_token = data["expire_token"]

    if model.roles:
      role_ids = [role.id for role in model.roles]
      role_repo = RoleRepo(db=db)
      model.permissions = role_repo.get_permissions(role_ids)

    return model
  except Exception as e:
    raise BadRequest400(str(e), e)


def get_cred_notif(browse_queries: BrowseSchema, db: Session, cred: dict, clear: bool = False):
  try:
    username = cred.get("username")
    if clear:
      db.query(Notification).filter(Notification.username == username).update({Notification.is_read: True})
      db.commit()

    data = select().filter(Notification.username == username)
    model = {
      "id"         : Notification.id,
      "username"   : Notification.username,
      "user_id"    : Notification.user_id,
      "is_read"    : Notification.is_read,
      "app"        : Notification.app,
      "title"      : Notification.title,
      "description": Notification.description,
      "path"       : Notification.path,
      "type"       : Notification.type,
      "color"      : Notification.color,
      "icon"       : Notification.icon,
      "created_at" : Notification.created_at,
      "updated_at" : Notification.updated_at,
    }
    data = browse(browse_queries=browse_queries, model=model, query=data, db=db)

    read   = db.query(Notification).filter(Notification.username == username, Notification.is_read.is_(True)).count()
    unread = db.query(Notification).filter(Notification.username == username, Notification.is_read.is_(False)).count()
    return {"read": read, "unread": unread, "all": read + unread, "items": data}
  except Exception as e:
    raise BadRequest400(str(e), e)


def get_cred_fav_menu(request: FavMenu, db: Session, cred: dict):
  username = cred.get("username")
  model = db.query(Model.menu_favorites).filter(Model.username == username).first()
  if not model:
    raise NotFound404(message=f"Data {Model.__tablename__} not Found")
  if request:
    try:
      db.query(Model).filter(Model.username == username).update({Model.menu_favorites: request.menu_favorites})
      db.commit()
      model = db.query(Model).filter(Model.username == username).first()
    except Exception as e:
      db.rollback()
      raise BadRequest400(str(e))
  return model


def delete(request: BulkId, id: int | None, db: Session, cred: dict):
  return soft_delete(request=request, id=id, db=db, model=Model, cred=cred, type="delete")


def restore(request: BulkId, id: int | None, db: Session, cred: dict):
  return soft_delete(request=request, id=id, db=db, model=Model, cred=cred, type="restore")


def get_signature(email: str, sign_type: str, db: Session):
  model = db.query(Model.name, Model.title, Model.signatures, Model.storage_signatures).filter(Model.email == email).first()
  if not model:
    raise NotFound404(message=f"Data {Model.__tablename__} not found")

  signature   = model.signatures.get(sign_type) if model.signatures else ""
  storage_id  = model.storage_signatures.get(sign_type) if model.storage_signatures else ""
  name        = model.name if model.name else email
  title       = model.title if model.title else ""
  return name, title, signature, storage_id


def get_msal_account_details(email: str, access_token: str) -> dict:
  fields = "displayName,companyName,mail,mobilePhone,jobTitle,officeLocation,department"
  url = f"https://graph.microsoft.com/v1.0/users?$filter=mail eq '{email}'&$select={fields}"
  headers = {"Authorization": f"Bearer {access_token}"}
  response = requests.get(url, headers=headers)
  if response.status_code != 200:
    raise BadRequest400(f"Error fetching user details: {response.status_code} - {response.text}")
  data = response.json()
  if "value" in data and len(data["value"]) > 0:
    return data["value"][0]
  raise NotFound404("User not found with the provided email")