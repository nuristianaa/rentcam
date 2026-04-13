# from typing import Dict, Any
import mimetypes
from typing import Annotated

from app.auth.auth_basic import basic_auth
from app.auth.oauth2 import check_jwt, check_permission, get_cred
from db.database import get_db
from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from utils.helpers.number_text import class2json
from utils.repo.queries import BrowseSchema, BulkId, browse_query
from utils.responses import BadRequest400, Forbidden403, NotFound404, res_success
from utils.storage.factory import get_active_storage
from .models import (
  ConstAdditionalPermissions,
  ConstType,
)
from .models import User as BaseModel
from .schema import ResetPass, UserCreate, UserWithCred
from .service.get import delete, get_id, get_index, get_msal_account_details, get_signature, get_users_by_role, restore
from .service.store import create, post_pict, reset_pass, update, update_sign
from app.auth.role.models import Role

path = "auth/users"
router = APIRouter(prefix=f"/v1/{path}", tags=[path], dependencies=[])
# storage = get_active_storage("STATIC_1")

# PUBLIC SIGNUP ENDPOINT
@router.post("/public")
def public_signup(request: UserCreate, db: Annotated[Session, Depends(get_db)]):
  # Get default user role ID dynamically
  user_role = db.query(Role).filter_by(name="user").first()
  default_user_role_id = user_role.id if user_role else 4
  
  # role_ids default ke user role jika tidak diisi
  if not request.role_ids:
    request.role_ids = [default_user_role_id]

  # additional_permissions default ke basic_auth
  if not request.additional_permissions:
    request.additional_permissions = ConstAdditionalPermissions.basic_auth

  data = create(request, db, cred={"username": "public"})
  return res_success(data=data, db=db)


# BROWSE
@router.get("")
def browse(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
  const_list: ConstType | None = None,
):
  check_permission(cred=cred, db=db, module=f"{path}-browse")
  if const_list:
    if const_list == ConstType.additional_permissions:
      data = class2json(ConstAdditionalPermissions)
      data = [
          {"code": item, "label": str(item).replace("_", " ").upper()}
          for item in data
      ]
  else:
    data = get_index(db, browse_queries)
  return res_success(data=data)

@router.get("/role/{role_id}")
def getUsersByRole(
  browse_queries: Annotated[BrowseSchema, Depends(browse_query)],
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
  role_id:int
):
  try:
    return get_users_by_role(role_id=role_id, db=db, browse_queries=browse_queries)
  except Exception as e:
    raise BadRequest400(str(e), e) from e

@router.get("/signature")
def signature(
  email: str,
  token: str,
  db: Annotated[Session, Depends(get_db)],
) -> StreamingResponse:
  if check_jwt(token):
    username, title, path, storage_id = get_signature(email, "default", db)

    file_data = None
    mime_type = None
    if path:
      storage = get_active_storage(storage_id=storage_id)
      file_data = storage.download_file(file_path=path)
      mime_type, _ = mimetypes.guess_type(path)

    mime_type = mime_type or "application/octet-stream"

    return StreamingResponse(
      iter([file_data]),  # type: ignore
      media_type=mime_type,
      headers={
        "Content-Disposition": f"inline; filename={path}",
        "X-Username": username,
        "X-UserTitle": title,
      },
    )
  else:
    raise Forbidden403("Invalid token")


@router.get("/signature-stamp")
def signature_stamp(
  email: str,
  token: str,
  db: Annotated[Session, Depends(get_db)],
) -> StreamingResponse:
  if check_jwt(token):
    username, title, path, storage_id = get_signature(email, "with_stamp", db)

    file_data = None
    mime_type = None
    if path:
      storage = get_active_storage(storage_id=storage_id)
      file_data = storage.download_file(file_path=path)
      mime_type, _ = mimetypes.guess_type(path)

    mime_type = mime_type or "application/octet-stream"

    return StreamingResponse(
      iter([file_data]),  # type: ignore
      media_type=mime_type,
      headers={
        "Content-Disposition": f"inline; filename={path}",
        "X-Username": username,
        "X-UserTitle": title,
      },
    )
  else:
    raise Forbidden403("Invalid token")


@router.get("/msal-account-details")
def msal_account_details(
  db: Annotated[Session, Depends(get_db)], cred: Annotated[dict, Depends(get_cred)], email: str, token: str
):
  check_permission(cred=cred, db=db, module=f"{path}-update")
  data = get_msal_account_details(email=email, access_token=token)
  return res_success(data=data)


# READ
@router.get("/{id}")
def browse_id(
  id: int,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
):
  check_permission(cred=cred, db=db, module=f"{path}-read")
  data = get_id(id, db)
  return res_success(data=data)


# CREATE
@router.post("")
def post_create(
  request: UserCreate,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
):
  check_permission(cred=cred, db=db, module=f"{path}-create")
  data = create(request, db, cred)
  return res_success(data=data, db=db)


# UPDATE
@router.put("/{id}")
def put_update(
  id: int,
  request: UserWithCred,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
):
  check_permission(cred=cred, db=db, module=f"{path}-update")
  data = update(id, request, db, cred)
  return res_success(data=data, db=db)


@router.post("/{id}/update-sign")
async def post_update_sign(
  id: int,
  cred: Annotated[dict, Depends(get_cred)],
  db: Annotated[Session, Depends(get_db)],
  sign_file: UploadFile | None = File(None),
  sign_with_stamp_file: UploadFile | None = File(None),
):
  sign_contents = None
  sign_type = ""
  if sign_file:
    sign_contents = await sign_file.read()
    filesize = len(sign_contents)
    max_size = 3 * 1024 * 1024
    if filesize > max_size:
      raise BadRequest400("Max filesize: 3 Mb!")
    if sign_file.content_type:
      sign_type = sign_file.content_type

  sign_with_stamp_contents = None
  sign_with_stamp_type = ""
  if sign_with_stamp_file:
    sign_with_stamp_contents = await sign_with_stamp_file.read()
    filesize = len(sign_with_stamp_contents)
    max_size = 3 * 1024 * 1024
    if filesize > max_size:
      raise BadRequest400("Max filesize: 3 Mb!")
    if sign_with_stamp_file.content_type:
      sign_with_stamp_type = sign_with_stamp_file.content_type

  files = {
    "sign": {"file": sign_contents, "type": sign_type},
    "sign_with_stamp": {"file": sign_with_stamp_contents, "type": sign_with_stamp_type},
  }

  data = update_sign(id=id, db=db, cred=cred, files=files)
  return res_success(data=data, db=db)

@router.post("/apply-stamps")
async def post_apply_stamps(
  request: Request,
  cred: Annotated[dict, Depends(get_cred)],
  db: Annotated[Session, Depends(get_db)],
  sign_file: UploadFile | None = File(None),
  sign_with_stamp_file: UploadFile | None = File(None),
):

  form = await request.form()
  ids = []
  if form.get("type") == 'vendors':
    if form.get("vendors"):
      vendors = form.get("vendors").split(',')
      ids = db.execute(select(BaseModel.id).where(BaseModel.vendors.in_(vendors), BaseModel.deleted_at.is_(None))).scalars().all()
  elif form.get("type") == 'not_vendors' and form.get("users"):
    ids = form.get("users").split(',')

  sign_contents = None
  sign_type = ""
  if sign_file:
    sign_contents = await sign_file.read()
    filesize = len(sign_contents)
    max_size = 3 * 1024 * 1024
    if filesize > max_size:
      raise BadRequest400("Max filesize: 3 Mb!")
    if sign_file.content_type:
      sign_type = sign_file.content_type

  sign_with_stamp_contents = None
  sign_with_stamp_type = ""
  if sign_with_stamp_file:
    sign_with_stamp_contents = await sign_with_stamp_file.read()
    filesize = len(sign_with_stamp_contents)
    max_size = 3 * 1024 * 1024
    if filesize > max_size:
      raise BadRequest400("Max filesize: 3 Mb!")
    if sign_with_stamp_file.content_type:
      sign_with_stamp_type = sign_with_stamp_file.content_type

  files = {
    "sign": {"file": sign_contents, "type": sign_type},
    "sign_with_stamp": {"file": sign_with_stamp_contents, "type": sign_with_stamp_type},
  }

  data = None
  res = []
  for id in ids:
    data = update_sign(id=id, db=db, cred=cred, files=files)
    res.append(data)

  return res_success(data=res, db=db)



@router.post("/{id}/update-avatar")
async def post_update_avatar(
  id: int,
  cred: Annotated[dict, Depends(get_cred)],
  db: Annotated[Session, Depends(get_db)],
  file: UploadFile | None = File(None),
):
  if file:
    contents = await file.read()
    content_type = file.content_type if file.content_type else 'image/png'
    filesize = len(contents)
    max_size = 10 * 1024 * 1024
    if filesize > max_size:
        raise BadRequest400(f"Max filesize: {10} Mb!")
    user_id = id
    data = post_pict(id=user_id, db=db, cred=cred, file=contents, content_type=content_type)
    return res_success(data=data, db=db)


# RESET PASS
@router.put("/{id}/reset-password")
def put_reset_pass(
  id: int,
  request: ResetPass,
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
):
  check_permission(cred=cred, db=db, module=f"{path}-update")
  data = reset_pass(id, request, db, cred)
  return res_success(data=data, db=db)


# DELETE & RESTORE
@router.delete("/delete")
def r_delete(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
  request: BulkId,
  id: int | None = None,
):
  check_permission(cred=cred, db=db, module=f"{path}-delete")
  data = delete(request, id, db, cred)
  return res_success(data=data, db=db)


@router.delete("/restore")
def r_restore(
  db: Annotated[Session, Depends(get_db)],
  cred: Annotated[dict, Depends(get_cred)],
  request: BulkId,
  id: int | None = None,
):
  check_permission(cred=cred, db=db, module=f"{path}-restore")
  data = restore(request, id, db, cred)
  return res_success(data=data, db=db)


# BASIC AUTH UPDATE SIGN FROM POWER APPS
@router.post("/{email}/update-sign-by-email")
async def post_update_sign_by_email(
  email: str,
  cred: Annotated[dict, Depends(basic_auth)],
  db: Annotated[Session, Depends(get_db)],
  sign_file: UploadFile | None = File(None),
  sign_with_stamp_file: UploadFile | None = File(None),
):
  sign_contents = None
  sign_type = ""
  if sign_file:
    sign_contents = await sign_file.read()
    filesize = len(sign_contents)
    max_size = 3 * 1024 * 1024
    if filesize > max_size:
      raise BadRequest400("Max filesize: 3 Mb!")
    if sign_file.content_type:
      sign_type = sign_file.content_type

  sign_with_stamp_contents = None
  sign_with_stamp_type = ""
  if sign_with_stamp_file:
    sign_with_stamp_contents = await sign_with_stamp_file.read()
    filesize = len(sign_with_stamp_contents)
    max_size = 3 * 1024 * 1024
    if filesize > max_size:
      raise BadRequest400("Max filesize: 3 Mb!")
    if sign_with_stamp_file.content_type:
      sign_with_stamp_type = sign_with_stamp_file.content_type

  files = {
    "sign": {"file": sign_contents, "type": sign_type},
    "sign_with_stamp": {"file": sign_with_stamp_contents, "type": sign_with_stamp_type},
  }
  id = db.query(BaseModel.id).filter(BaseModel.email == email).scalar()
  if id is None:
    raise NotFound404("User not found")

  data = update_sign(id=id, db=db, cred=cred, files=files)
  return res_success(data=data, db=db)
