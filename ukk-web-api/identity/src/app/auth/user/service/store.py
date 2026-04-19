# from fastapi.encoders import jsonable_encoder
from app.auth.role.models import Role
from app.auth.user_role.models import UserRole
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.helpers.hash import bcrypt, verify
from utils.helpers.number_text import generate_strong_password
from utils.notification import ReqNotif, send_notif
from utils.responses import BadRequest400, NotFound404
from utils.storage.factory import get_active_storage

from ..models import User as Model, ConstAdditionalPermissions
from ..schema import (
  ChangePass,
  ResetPass,
  UserBase,
  UserCreate,
  UserWithCred,
  validate_password,
)

module_name = "User"
storage = get_active_storage()


def reset_pass(id: int, request: ResetPass, db: Session, cred: dict):
  username = cred.get("username")
  data = db.query(Model).filter(Model.id == id, Model.deleted_at.is_(None)).first()
  if data is None:
    raise NotFound404()

  before = jsonable_encoder(data)

  try:
    passw = bcrypt(request.password)
    db.query(Model).filter(Model.id == id).update({Model.password: passw, Model.updated_by: username})
    db.flush()
    db.refresh(data)

    log_data = jsonable_encoder(data)
    log_name = f"{log_data.get('name')}"
    data_log = define_datalog(name=log_name, before=before, after=log_data)
    logs(type="update", model=Model, cred=cred, data=data_log)

    if data and data.username:
      req_notif = ReqNotif(
        usernames=[data.username],
        title="Password Changed",
        description="Your password has been changed by administrator",
        path="/home",
      )
      send_notif(req_notif)
    return data
  except Exception as e:
    raise BadRequest400(str(e), e)


def create(request: UserCreate, db: Session, cred: dict):
  username = cred.get("username", "public")
  if request.password:
    validate_password(request.password)
  else:
    request.password = generate_strong_password(25)

  # Enforce public signup defaults when using the public registration flow.
  if username == "public":
    if not request.additional_permissions:
      request.additional_permissions = ConstAdditionalPermissions.basic_auth

  request.password = bcrypt(request.password)
  values = request.model_dump(exclude={"role_ids"})
  values["created_by"] = username

  try:
    data = db.execute(insert(Model).values(values).returning(Model)).scalars().first()
    db.flush()

    if not data:
      raise BadRequest400()

    # Get default user role ID dynamically
    user_role = db.query(Role).filter_by(name="user").first()
    default_user_role_id = user_role.id if user_role else 4
    
    # Jika role_ids tidak diisi, assign default role user
    role_ids = request.role_ids if request.role_ids else [default_user_role_id]
    db.execute(insert(UserRole), [{"user_id": data.id, "role_id": role_id} for role_id in role_ids])

    db.refresh(data)

    data = jsonable_encoder(data)
    log_name = f"{data.get('name')}"
    data_log = define_datalog(name=log_name, after=data)
    # Only log if cred has token (not public)
    if cred.get("token"):
      logs(type="create", model=Model, cred=cred, data=data_log)
    return data
  except Exception as e:
    raise BadRequest400(str(e), e)


def update(id: int, request: UserWithCred, db: Session, cred: dict):
  data = db.query(Model).filter(Model.id == id, Model.deleted_at.is_(None)).first()
  if data is None:
    raise NotFound404()

  before = jsonable_encoder(data)

  try:
    username = cred.get("username")
    values = request.model_dump(exclude={"role_ids"}, exclude_unset=True)
    values["updated_by"] = username

    db.execute(sql_update(Model).where(Model.id == id).values(values))
    db.flush()

    if request.role_ids:
      roles = db.query(Role).filter(Role.id.in_(request.role_ids)).all()
      data.roles = roles

    db.refresh(data)

    data = jsonable_encoder(data)
    log_name = f"{data.get('name')}"
    data_log = define_datalog(name=log_name, before=before, after=data)
    logs(type="update", model=Model, cred=cred, data=data_log)
    return data
  except Exception as e:
    raise BadRequest400(str(e), e)


def update_by_cred(request: UserBase, db: Session, cred: dict):
  username = cred.get("username")
  data = db.query(Model).filter(Model.username == username, Model.deleted_at.is_(None)).first()
  if data is None:
    raise NotFound404()

  before = jsonable_encoder(data)

  try:
    values = request.model_dump(exclude_unset=True)
    # values = {**data.__dict__, **request.model_dump(exclude_unset=True)}
    values["updated_by"] = username
    db.execute(sql_update(Model).where(Model.username == username).values(values))
    db.flush()
    db.refresh(data)

    data = jsonable_encoder(data)
    log_name = f"{data.get('name')}"
    data_log = define_datalog(name=log_name, before=before, after=data)
    logs(type="update", model=Model, cred=cred, data=data_log)
    return data
  except Exception as e:
    raise BadRequest400(str(e), e)


def update_password(request: ChangePass, db: Session, cred: dict):
  username = cred.get("username", "")
  data = db.query(Model).filter(Model.username == username, Model.deleted_at.is_(None)).first()
  if data is None:
    raise NotFound404()

  before = jsonable_encoder(data)

  try:
    if data and verify(data.password, request.current_password):
      passw = bcrypt(request.password)
      db.query(Model).filter(Model.username == username).update({Model.password: passw, Model.updated_by: username})
      db.flush()
      db.refresh(data)

      data = jsonable_encoder(data)
      log_name = f"{data.get('name')}"
      data_log = define_datalog(name=log_name, before=before, after=data)
      logs(type="update", model=Model, cred=cred, data=data_log)

      req_notif = ReqNotif(
        usernames=[username],
        title="Password Changed",
        description="Your password has been changed",
        path="/home",
      )
      send_notif(req_notif)
      return data
    raise BadRequest400("Current password did not match")
  except Exception as e:
    raise BadRequest400(str(e), e)


def post_pict(id: int, db: Session, cred: dict, file: bytes, content_type: str):
  data = db.query(Model).filter(Model.id == id, Model.deleted_at.is_(None)).first()
  if data is None:
    raise NotFound404()

  before = jsonable_encoder(data)

  try:
    path = f"users/profile_picture_user{id}"
    pict = storage.upload_file(file_path=path, data=file, content_type=content_type, is_public=False)
    storage_id = pict.get("id", None)
    db.query(Model).filter(Model.id == id).update(
      {Model.profile_picture: pict.get("path", None)}
    )
    db.commit()

    data = jsonable_encoder(data)
    log_name = f"{data.get('name')}"
    data_log = define_datalog(name=log_name, before=before, after=data)
    logs(type="update", model=Model, cred=cred, data=data_log)

    return data
  except Exception as e:
    raise BadRequest400(str(e), e)


def update_sign(id: int, db: Session, cred: dict, files: dict):
    try:
        username = cred.get("username")

        data = db.execute(
            select(Model).where(Model.id == id, Model.deleted_at.is_(None))
        ).scalars().first()

        if data is None:
            raise NotFound404()

        # before = jsonable_encoder(data)

        # Ambil existing value
        signature = {
            "default": data.signatures.get("default") if data.signatures else None,
            "with_stamp": data.signatures.get("with_stamp") if data.signatures else None,
        }

        storage_signatures = {
            "default": data.storage_signatures.get("default") if data.storage_signatures else None,
            "with_stamp": data.storage_signatures.get("with_stamp") if data.storage_signatures else None,
        }

        # ====== PROSES UPLOAD FILE ========
        for key, value in files.items():
            file_bytes = value.get("file")
            content_type = value.get("type")

            if not file_bytes:
                continue  # skip kalau None / kosong

            if key == "sign":
                path = f"users/user_signature{id}"
            elif key == "sign_with_stamp":
                path = f"users/user_signature_with_stamp{id}"
            else:
                continue

            uploaded = storage.upload_file(
                file_path=path,
                data=file_bytes,
                content_type=content_type,
                is_public=False,
            )

            if key == "sign":
                signature["default"] = uploaded.get("path")
                storage_signatures["default"] = uploaded.get("id")
            else:
                signature["with_stamp"] = uploaded.get("path")
                storage_signatures["with_stamp"] = uploaded.get("id")

        clean_signature = {k: v for k, v in signature.items() if v is not None}
        clean_storage_signatures = {k: v for k, v in storage_signatures.items() if v is not None}


        update_data = {
            Model.updated_by: username,
            Model.signatures: clean_signature,
            Model.storage_signatures: clean_storage_signatures,
        }

        # ====== UPDATE DB ========
        db.query(Model).filter(Model.id == id).update(update_data)

        db.commit()
        db.refresh(data)

        # ====== LOGGING ========
        after = jsonable_encoder(data)
        print("DEBUG after update:", after)

        # data_log = define_datalog(name=data.name, before=before, after=after)
        # logs(type="update", model=Model, cred=cred, data=data_log)

        return after

    except Exception as e:
        raise BadRequest400(str(e), e)

