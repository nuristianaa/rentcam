import json
import time
import uuid
from contextlib import suppress
from typing import Any, Literal

import requests
from config.config import APP, getenv
from cryptography.fernet import Fernet
from fastapi.encoders import jsonable_encoder
from jose import jwt
from pydantic import BaseModel as PydanticBaseModel
from requests.auth import HTTPBasicAuth
from sqlalchemy import text
from sqlalchemy.orm import Session
from utils.helpers.trans_module import trans_module
from utils.responses import BadRequest400

appslug = "erpunais"
appname = "ERP-UNAIS"

ForeignValidationAction = Literal["update", "delete"]


######### MICROSERVICES #########
def gen_jwt(username: str = "system") -> str:
  SECRET_KEY = getenv("JWT_SECRET")
  FERNET_KEY = getenv("FERNET_KEY")
  fernet = Fernet(FERNET_KEY.encode())
  token_id = str(uuid.uuid4())  # Random unique string
  currentms = int(round(time.time() * 1000))
  expires = currentms + 10 * 60000
  encrypted_data = fernet.encrypt(f"{token_id}|{expires}".encode()).decode()
  to_encode = {
    "ed": encrypted_data,
    "sub": username,
    "user_id": 2,
    "username": username,
    "name": username,
    "companies": "all",
    "role_code": "superuser",
    "additional_permissions": "",
    "utc": currentms,
    "exp": expires,
    "device_id": None,
  }
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
  return encoded_jwt


def gen_jwt_wb_app(username: str = "system") -> str:
  JWT_SECRET_WB_APP = getenv("JWT_SECRET_WB_APP", "")
  currentms = int(round(time.time() * 1000))
  expires = currentms + 10 * 60000
  to_encode = {
    "sub": username,
    "user_id": 2,
    "username": username,
    "name": username,
    "companies": "",
    "role_code": "",
    "additional_permissions": "",
    "utc": currentms,
    "exp": expires,
    "device_id": None,
  }
  encoded_jwt = jwt.encode(to_encode, JWT_SECRET_WB_APP, algorithm="HS256")
  return encoded_jwt


def logs(
  *, type: str, model: Any, data: Any, cred: dict | None, db: Session | None = None, app: str | None = None, flag: str | None = None
) -> str:
  username = cred["username"] if cred else ""
  schema = (
      getattr(model, "__schema_app__", None)
      or model.__table__.schema
      or "public"
  )
  table = model.__table__.name
  bodyreq = []
  # 1. Prepare data
  if type in ["delete", "restore"] and db:
    items = db.query(model).where(model.id.in_(data)).all()
  elif isinstance(data, list):
    items = data
  else:
    items = [data]
  for item in items:
    req = {
      "app": app or APP,
      "type": type,
      "schema": schema,
      "module": table,
      "module_id": None,
      "name": None,
      "data": None,
      "username": username,
    }

    # Append flag
    _flag_value = flag if flag is not None else type
    if isinstance(item, dict):
      reordered = {"_flag": _flag_value, **item}
    else:
      data_dict = {k: v for k, v in vars(item).items() if not k.startswith("_")}
      reordered = {"_flag": _flag_value, **data_dict}
    item = reordered

    # Safely convert item to dict
    with suppress(Exception):
      item = jsonable_encoder(item)

    # Extract `module_id` from 'id', if available
    module_id = item.get("id") if isinstance(item, dict) else None
    if module_id is not None:
      req["module_id"] = str(module_id)

    # Save the entire item as data
    req["data"] = item
    # Try to get a meaningful name from known fields
    name_fields = [
      "code",
      "name",
      "number",
      "module",
      "do_code",
      "wo_code",
      "version",
      "unit_code",
      "truck_code",
      "he_code",
      "shipment_code",
      "nomination",
      "remark",
      "id",
    ]
    req["name"] = str(item)
    if isinstance(item, dict):
      for field in name_fields:
        if field in item and item[field]:
          req["name"] = str(item[field])
          break  # Stop at the first matching field
    bodyreq.append(req)

  token = cred["token"] if cred else None
  url = getenv("LOGS_URL", "http://localhost:8090/v1/audit-trails")
  if token is None:
    token = gen_jwt(username)
  headers = {"Authorization": f"Bearer {token}"}

  msg = "std repo logs: "
  try:
    if token:
      api = requests.post(url, headers=headers, json=bodyreq)
      response: dict = json.loads(api.content)
      msg += str(response)
  except Exception as e:
    msg += str(e)
  # print(bodyreq)
  return msg



def service_api_email(*, to: list[str], subject: str, body: str, bt: bool = False, cred: dict | None = None) -> str:
  token = cred["token"] if cred else gen_jwt()
  url = "v1/email"
  bodyreq = {"bt": bt, "company": "unais", "to": to, "subject": subject, "body": body}
  msg = "std repo email: "
  # do send email
  # print(msg)
  return msg


def save_document_history(id: str | int, cred: dict, data: dict) -> None:
  try:
    bodyreq = {
      "app": "crm",
      "module": data.get("ref_module"),
      "module_id": str(id),
      "template_id": str(data.get("template_id")) if data else None,
      "template_name": data.get("template_name") if data else None,
    }
    microservice(
      ep="v1/document-histories",
      cred=cred,
      app="main",
      method="POST",
      body=bodyreq,
    )
  except Exception as e:
    print("[Error] Pdf generator -> generate filaname: ", str(e))


def microservice(ep: str, cred: dict | None = None, app: str = "main", method: str = "GET", body: dict = None):  # type: ignore
  """
  return {
      'data': None,
      'status': {
        'code': 200,
        'message': str(e)
      }
    }
  """
  token = cred.get('token', None) if cred else None

  if app == "identity":
    baseurl = getenv("IDENTITY_URL", "http://localhost:8090/")
  elif app == "crm":
    baseurl = getenv("CRM_URL", "http://localhost:8091/")
  elif app == "engineering":
    baseurl = getenv("ENGINEERING_URL", "http://localhost:8092/")
  elif app == "finance":
    baseurl = getenv("FINANCE_URL", "http://localhost:8093/")
  elif app == "procurement":
    baseurl = getenv("PROCUREMENT_URL", "http://localhost:8094/")
  elif app == "project_management":
    baseurl = getenv("PROJECT_MANAGEMENT_URL", "http://localhost:8095/")
  elif app == "hris":
    baseurl = getenv("HRIS_URL", "http://localhost:8096/")
  url = f"{baseurl}{ep}"
  if token is None:
    token = gen_jwt()
  headers = {"Authorization": f"Bearer {token}"}

  try:
    if method == "GET":
      api = requests.get(url, headers=headers)
    if method == "POST":
      api = requests.post(url, headers=headers, json=body)
    return json.loads(api.content)
  except Exception as e:
    return {"data": None, "status": {"code": 400, "message": str(e)}}


def foreign_validation(
  db: Session,
  validation_fields: dict,
  action: ForeignValidationAction,
  data: Any | None = None,
  request: PydanticBaseModel | None = None,
  model: Any | None = None,
  id: int | str | None = None,
):
  """Main entry point for foreign validation (update or delete)."""
  if action == "update":
    return _update_foreign_validation(db=db, validation_fields=validation_fields, data=data, request=request)
  elif action == "delete":
    return _delete_foreign_validation(db=db, validation_fields=validation_fields, request=request, id=id, model=model)


def _update_foreign_validation(db: Session, validation_fields: dict, data: Any, request: PydanticBaseModel | None):
  """Validation logic for update."""
  # Convert ORM object -> dict (only DB columns)
  data_dict = {c.name: getattr(data, c.name) for c in data.__table__.columns} if data else {}

  # New values from request (exclude unset fields)
  values: dict = request.model_dump(exclude_unset=True) if request else {}

  for column, fields in validation_fields.items():
    old_value = data_dict.get(column)
    new_value = values.get(column)
    for field in fields:
      sql = text(f"""
        SELECT {field["column"]}
        FROM {field["model"]}
        WHERE {field["column"]} = :value AND deleted_at IS NULL
        LIMIT 1
      """)

      result = db.execute(sql, {"value": old_value}).scalar()
      if result is not None and new_value != result:
        field_label = trans_module(field["model"])
        raise BadRequest400(f"Cannot change data, {column} is already used in {field_label}")


def _delete_foreign_validation(db: Session, validation_fields: dict, request: Any, id: int | str | None, model: Any):
  """Validation logic for delete."""
  if request.id:
    items = db.query(model).where(model.id.in_(request.id)).all()
  elif id:
    items = db.query(model).where(model.id == id).all()
  else:
    raise BadRequest400("No data found")

  # Convert ORM object -> dict (only DB columns)
  values = [{c.name: getattr(item, c.name) for c in item.__table__.columns} for item in items]

  blocked = []

  for column, fields in validation_fields.items():
    for value in values:
      old_value = value.get(column)
      for field in fields:
        sql = text(f"""
          SELECT {field["column"]}
          FROM {field["model"]}
          WHERE {field["column"]} = :value AND deleted_at IS NULL
          LIMIT 1
        """)

        result = db.execute(sql, {"value": old_value}).scalar()
        if result:
          field_label = trans_module(field["model"])
          blocked.append(f"{column}={old_value} is already used in {field_label}")

  if blocked:
    msg = "\n".join(blocked)
    raise BadRequest400(f"Cannot delete some records:\n {msg}")


def send_event_notif(*, cred: dict, event_name: str, data: Any):
  """Handle notification based on event name in table Event Notification"""
  username = cred["username"] if cred else ""

  # Safely convert data to dict
  with suppress(Exception):
    data = jsonable_encoder(data)

  body = {
    **data,
    "app": APP,
    "event_name": event_name,
    "user": username,
  }
  microservice(
    ep="v1/auth/event-notifications/send?schedule_type=custom",
    cred=cred,
    app="main",
    method="POST",
    body=body,
  )

def send_crud_notif(type: str, model: Any, data: Any | None = None, cred: dict | None = None, label: str | None = None):
  """Handle CRUD notification based on event"""
  username = cred["username"] if cred else ""
  schema = model.__table__.schema or "public"
  table = model.__table__.name

  req = {
    "app": APP,
    "user": username,
    "schema": schema,
    "table": table,
    "type": type,
    "label": label
  }

  if data is None:
    microservice(
      ep="v1/auth/event-notifications/send?schedule_type=crud",
      cred=cred,
      app="main",
      method="POST",
      body=req,
    )
    return

  items = data if isinstance(data, list) else [data]

  for item in items:
    item = {k: v for k, v in vars(item).items() if not k.startswith("_")}

    # Safely convert item to dict
    with suppress(Exception):
      item = jsonable_encoder(item)

    # Extract `module_id` from 'id', if available
    module_id = item.get("id") if isinstance(item, dict) else None
    if module_id is not None:
      req["module_id"] = str(module_id)

    # Save the entire item as data
    req["data"] = item

    name_fields = [
      "code",
      "name",
      "number",
      "module",
      "do_code",
      "wo_code",
      "version",
      "unit_code",
      "truck_code",
      "he_code",
      "shipment_code",
      "nomination",
      "remark",
      "id",
    ]

    if isinstance(item, dict) and not label:
      for field in name_fields:
        if field in item and item[field]:
          req["label"] = str(item[field])
          break  # Stop at the first matching field

    microservice(
      ep="v1/auth/event-notifications/send?schedule_type=crud",
      cred=cred,
      app="main",
      method="POST",
      body=req,
    )
