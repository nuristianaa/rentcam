import re
import string
import time
import uuid
from datetime import date as date_type
from datetime import datetime as datetime_type
from typing import Any, Union, get_args, get_origin

from config import getenv
from cryptography.fernet import Fernet
from fastapi import Request
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from jose import jwt
from sqlalchemy import String, cast, or_, select
from sqlalchemy.orm import Session
from utils.audit_trail import define_datalog, logs
from utils.helpers.date import transform_query_partition
from utils.repo.queries import BulkId

appslug = "erpunais"
appname = "ERP-UNAIS"


class StdService:
  def __init__(self, db: Session, cred: dict | None, module_repo: Any) -> None:
    self.db = db
    self.cred = cred
    self.username = cred["username"] if cred else None
    self.user_id = cred.get("user_id") if cred else None
    self.module_repo = module_repo

  # ---------- STD_SERVICES ----------#
  def query_company(self, model: Any, query: Any = None, other_queries: Any = None):
    """Define query strictly show only their company"""
    if query is None:
      query = select()
    if not hasattr(model, "company_code"):
      return select()
    if hasattr(other_queries, "company_code") and other_queries.company_code:
      query = select().filter(model.company_code == other_queries.company_code)
    else:
      companies = None
      if self.cred and (companies_str := self.cred.get("companies", "")) and "all" not in companies_str:
        companies = companies_str.split(",")
      query = select()
      if companies:
        query = query.filter(model.company_code.in_(companies))
    return query

  def query_vendor(self, model: Any, query: Any = None, other_queries: Any = None, fields: list[str] | None = None):
    """Define query strictly show only their company"""
    if fields is None:
      fields = ["vendor_code"]
    if query is None:
      query = select()

    if not hasattr(model, "vendor_code"):
      return query

    if hasattr(other_queries, "vendor_code") and other_queries.vendor_code:
      ors = [getattr(model, field) == other_queries.vendor_code for field in fields]
      query = query.where(or_(*ors))
    else:
      vendors = None
      if self.cred and (vendors_str := self.cred.get("vendors", "")) and "all" not in vendors_str:
        vendors = vendors_str.split(",")
      query = select()
      if vendors:
        query = query.filter(model.vendor_code.in_(vendors))
        ors = [getattr(model, field).in_(vendors) for field in fields]
        query = query.where(or_(*ors))
    return query

  def query_partition(self, request: Request, model: Any, query: Any, date_columns: list[str]):
    """Assign query created_at based on query dates."""
    date_from, date_to = transform_query_partition(date_columns=date_columns, query_list=request.query_params.values())
    if query is None:
      query = select()
    query = query.where(model.created_at >= date_from, model.created_at <= date_to)
    return query

  def get_id(self, id: str | int):
    """Returns data based on data id."""
    return self.module_repo.get_id(id)

  def delete(self, req: BulkId, id: str | int | None):
    ids: Any = req.id or [id]
    return self.module_repo.soft_delete(ids=ids, cred=self.cred, action="delete")

  def restore(self, req: BulkId, id: str | int | None):
    ids: Any = req.id or [id]
    return self.module_repo.soft_delete(ids=ids, cred=self.cred, action="restore")

  def exec_bulk_store(self, model: Any, req: list[Any]):
    failed, updates, inserts = [], [], []
    update_logs, insert_logs = [], []

    # 0. Mappings
    keys = [v.id for v in req]
    existing = self.db.query(model).filter(cast(model.id, String).in_(keys)).all()
    existing_map = {(str(r.id)): r for r in existing}

    # 1. Prepare Values
    for v in req:
      values = v.model_dump()
      try:
        key = str(v.id)
        if key in existing_map:  # update
          r_data = existing_map[key]
          existing = jsonable_encoder(r_data)
          values["id"] = existing.get("id")
          values["updated_by"] = self.username
          values["deleted_at"] = None
          updates.append(values)
          log_name = f"{values.get('code')}"  # Audit trails log name
          update_logs.append(define_datalog(name=log_name, before=existing, after=values))
        else:  # insert
          values["created_by"] = self.username
          inserts.append(values)
          log_name = f"{values.get('code')}"  # Audit trails log name
          insert_logs.append(define_datalog(name=log_name, after=values))
      except Exception as e:
        values["msg"] = str(e)
        failed.append(values)

    # 2. Execute Logs
    if inserts and len(inserts) > 0:
      self.module_repo.bulk_store(values=inserts, action="insert")
      logs(type="create", model=model, cred=self.cred, data=insert_logs)
    if updates and len(updates) > 0:
      self.module_repo.bulk_store(values=updates, action="update")
      logs(type="update", model=model, cred=self.cred, data=update_logs)

    return {"success": f"{len(inserts)} data inserted & {len(updates)} data updated", "failed": failed}  
  
  # code generator
  def generate_code(self, model: Any, req: BaseModel) -> str:
    config = getattr(model, "__code_config__", None)
    if not config:
      raise ValueError(f"Model {model.__name__} is missing 'code_config' attribute.")

    mapping = config.get("mapping", {})
    pattern = config.get("pattern", "")
    field = config.get("field", "code")

    pattern_keys = [t[1] for t in string.Formatter().parse(pattern) if t[1] is not None]

    format_args = {}

    # Build code prefix
    for key in pattern_keys:
      if key == "_serial":
        continue

      rule = mapping.get(key)
      if not rule:
        raise ValueError(f"Pattern key '{key}' is missing from 'mapping' config.")

      field_name = rule.get("key")

      # Get value from pydantic instance
      val = getattr(req, field_name, None)

      # Get type from pydantic class
      field_type = self._get_pydantic_field_type(req, field_name)

      # Check requirement
      if val is None:
        raise ValueError(f"Field '{field_name}' is required for code generation but is None/Empty.")

      format_args[key] = self._apply_format_generator(value=val, fmt_rule=rule.get("format"), field_type=field_type)

    # Search for get serial
    search_pattern = pattern.format(_serial="%", **format_args)

    last_code = self.module_repo.get_last_serial_code_by_pattern(model, field, search_pattern)

    new_serial = 1
    if last_code:
      try:
        safe_args = {k: re.escape(v) for k, v in format_args.items()}
        regex_pattern_str = pattern.format(_serial=r"(?P<_serial>\d+)", **safe_args)
        regex_pattern_str = f"^{regex_pattern_str}"
        match = re.match(regex_pattern_str, last_code)
        if match:
          last_serial_str = match.group("_serial")
          new_serial = int(last_serial_str) + 1
      except ValueError:
        new_serial = 1

    serial_rule = mapping.get("_serial", {})
    digit_len = serial_rule.get("format", 4)

    format_args["_serial"] = str(new_serial).zfill(digit_len)

    return pattern.format(**format_args)

  def _get_pydantic_field_type(self, req: BaseModel | type[BaseModel], field_name: str):
    """
    Safely gets the type of a field from a Pydantic model class or instance
    """
    req_class = req if isinstance(req, type) and issubclass(req, BaseModel) else type(req)

    field_info = req_class.model_fields.get(field_name)  # type: ignore
    if field_info is None:
      return None

    annotation = field_info.annotation
    if get_origin(annotation) is Union:
      args = get_args(annotation)
      non_none = [a for a in args if a is not type(None)]
      return non_none[0] if non_none else None

    return annotation

  def _apply_format_generator(self, value: Any, fmt_rule: Any, field_type: Any) -> str:
    """
    Formats a signel value based on its type and the mapping rule.
    """
    if value is None:
      return ""

    # Date and datetime format
    if field_type in (date_type, datetime_type):
      fmt = fmt_rule if isinstance(fmt_rule, str) and fmt_rule else "%Y-%m-%d"
      return value.strftime(fmt)

    # String
    if isinstance(value, str):
      if fmt_rule == "uppercase":
        return str(value).upper()
      elif fmt_rule == "lowercase":
        return str(value).lower()
      else:
        return str(value)

    # Default/number
    return str(value)

# ---------- GENERATE JWT ----------#
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