import json
from contextlib import suppress
from typing import Any

import requests
from config import APP, getenv
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session


def logs(
  *,
  type: str,
  model: Any,
  data: Any,
  cred: dict | None,
  app: str | None = None,
  flag: str | None = None,
  schema: str | None = None,
  # db: Session|None = None,
) -> str:
  from utils.std_service import gen_jwt

  username = cred["username"] if cred else ""
  schema_fix = (
      getattr(model, "__schema_app__", None)
      or model.__table__.schema
      or "public"
  )
  table = model.__table__.name
  bodyreq = []
  items = data if isinstance(data, list) else [data]
  for item in items:
    req = {
      "app": app or APP,
      "type": type,
      "schema": schema if schema else schema_fix,
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

    # Save the entire item as data
    req["module_id"] = str(item.get("id") if isinstance(item, dict) else "")
    req["data"] = item
    req["name"] = extract_name(item)
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


# NEW for define data_before & after
def define_datalog(*, name: str | None, before: dict | None = None, after: dict | None = None):
  before = before or {}
  after = after or {}
  id_ = before.get("id", None) or after.get("id", None) or ""

  # keep only changed or new keys
  final = {}
  for k, v in after.items():
    if before.get(k) != v:
      final[k] = v

  final["id"] = id_
  final["_name"] = name
  final["_before"] = before

  return final


def extract_name(item: dict):
  # Try to get a meaningful name from known fields
  name_fields = [
    "_name",
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
  name = ""
  if isinstance(item, dict):
    for field in name_fields:
      if field in item and item[field]:
        name = str(item[field])
        break  # Stop at the first matching field
  return name


def build_datalog(
  db: Session,
  action_type: str,
  model: Any,
  ids: list[int | str] | list[int | str | None] | str | int | None = None,
  before: list[dict] | dict | None = None,
  after: list[dict] | dict | None = None,
):
  data_log = []
  ids = [ids] if isinstance(ids, (int|str)) else ids
  try:
    if after:
      after = [after] if isinstance(after, dict) else after
      before = [before] if isinstance(before, dict) else before
      for index, data in enumerate(after):
        if action_type == "create":
          data_log.append(define_datalog(name=extract_name(data), after=data))
        elif action_type == "update" and before:
          data_log.append(define_datalog(name=extract_name(data), after=data, before=before[index]))
    else:
      items_raw = db.query(model).where(model.id.in_(ids)).all()
      for item in items_raw:
        item_dict = jsonable_encoder(item)
        if action_type == "create":
          row = define_datalog(name=extract_name(item_dict), after=item_dict)
        elif action_type == "update":
          before = before[0] if isinstance(before, list) else before
          row = define_datalog(name=extract_name(item_dict), before=before, after=item_dict)
        else:
          row = define_datalog(name=extract_name(item_dict), before=item_dict)

        data_log.append(row)
    return data_log
  except Exception as e:
    raise e
