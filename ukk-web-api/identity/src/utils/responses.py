import re
import traceback
from typing import Any

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session

# from config import is_dev

def res_content(request: Request, status: int, msg: Any, detail: Any = None):
  error_code = f'{status}'
  if status == 400: error_code = 'Bad Request (400)'
  if status == 401: error_code = 'Unauthorized (401)'
  if status == 403: error_code = 'Forbidden (403)'
  if status == 404: error_code = 'NotFound (404)'
  if status == 406: error_code = 'Not Acceptable (406)'
  if status == 422: error_code = 'Unprocessable Content (422)'

  if status in [406, 422]:
    try:
      msg = 'Request Error: '
      for d in detail:
        if d.get('msg', None): msg += d['msg'] + ' '
        else:
          if d.get('type', None):
            msg += d['type'] + ': '
          for loc in d.loc:
            msg += loc + ', '
          if d.get('ctx', None) and d['ctx'].get('reason', None):
            msg += d['ctx']['reason'] + ' '
    except: ''

  user_agent = request.headers.get("user-agent", "Unknown")
  return {
    'data': None,
    'status': {
      'code': status,
      'message': str(msg)[:150],
      'full_message': msg,
      'error_code': error_code,
      'error_detail': detail,
      'user_agent': user_agent
    }
  }


def res_success(*, data: Any = None, db: Session | None = None, exec_commit: bool = True, status: int = 200):
  try: items = jsonable_encoder(data)
  except: items = data
  if exec_commit and db: db.commit()
  return {
    'data': items,
    'status': {
      'code': status,
      'message': 'success',
      'error_code': '',
      'error_detail': None
    }
  }


def res_rate_limit(request: Request) -> JSONResponse:
  path = request.url.path
  if path == '/check-permission':
    msg = 'Rate limit exceeded.'
    return JSONResponse(status_code=200, content={"message": msg}, headers={'X-Auth-Message': msg})
  else:
    msg = 'The system is currently busy due to too many requests. Please try again later.'
    return JSONResponse(status_code=429, content=res_content(request, 429, msg))


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
  return res_rate_limit(request=request)


def _match(pattern: str, text: str, message_template: str):
  m = re.search(pattern, text)
  if m:
    try:
      return message_template.format(*m.groups())
    except Exception:
      return message_template
  return None


def readable_db_error(error_msg: str) -> str:
  """Return human-readable description for common PostgreSQL errors."""

  patterns = [
    # Constraint violations
    (r"NotNullViolation", lambda m: _match(r'null value in column "(.+?)" of relation "(.+?)"', error_msg,
                                            "The column '{0}' in table '{1}' cannot be empty (NOT NULL constraint).")),
    (r"UniqueViolation", lambda m: _match(r'Key \((.+?)\)=\((.+?)\) already exists', error_msg,
                                          "Duplicate value '{1}' found for unique field '{0}'.")),
    (r"ForeignKeyViolation", lambda m: _match(r'Key \((.+?)\)=\((.+?)\) is not present in table "(.+?)"', error_msg,
                                              "The value '{1}' in '{0}' does not exist in referenced table '{2}'.")),
    (r"CheckViolation", lambda m: "A CHECK constraint failed for one of the columns."),
    (r"ExclusionViolation", lambda m: "An exclusion constraint was violated (conflicting range or condition)."),

    # Schema/name errors
    (r"UndefinedTable", lambda m: _match(r'relation "(.+?)" does not exist', error_msg,
                                          "The table '{0}' does not exist in the database.")),
    (r"UndefinedColumn", lambda m: _match(r'column "(.+?)" does not exist', error_msg,
                                          "The column '{0}' does not exist in the table.")),
    (r"DuplicateColumn", lambda m: _match(r'column "(.+?)" of relation "(.+?)" already exists', error_msg,
                                          "The column '{0}' already exists in table '{1}'.")),
    (r"DuplicateTable", lambda m: _match(r'relation "(.+?)" already exists', error_msg,
                                          "The table '{0}' already exists.")),

    # Data exceptions
    (r"InvalidTextRepresentation", lambda m: "Invalid data format — incompatible value for the target column."),
    (r"NumericValueOutOfRange", lambda m: "A numeric value is too large or small for its column."),
    (r"DivisionByZero", lambda m: "Division by zero occurred during query execution."),
    (r"StringDataRightTruncation", lambda m: "Input string too long for the column size limit."),

    # Connection/database issues
    (r"InvalidCatalogName", lambda m: _match(r'database "(.+?)" does not exist', error_msg,
                                              "The database '{0}' does not exist.")),
    (r"ConnectionException", lambda m: "Database connection failed or was lost."),
    (r"OperationalError", lambda m: "Operational database error — check connection or server availability."),

    # Transaction & concurrency
    (r"DeadlockDetected", lambda m: "Deadlock detected between concurrent transactions."),
    (r"SerializationFailure", lambda m: "Transaction serialization failure — please retry."),

    # Permission/security
    (r"InsufficientPrivilege", lambda m: "Permission denied — user lacks required privilege."),
    (r"InvalidAuthorizationSpecification", lambda m: "Invalid database credentials or authorization failed."),

    # Resource limits
    (r"OutOfMemory", lambda m: "Database ran out of memory."),
    (r"DiskFull", lambda m: "Database storage is full."),
    (r"LockNotAvailable", lambda m: "Could not acquire the required lock — resource busy."),
  ]

  for key, handler in patterns:
    if key in error_msg:
      result = handler(error_msg)
      if result:
        return result

  # Fallbacks for NA metadata or unknown errors
  if "NA" in error_msg:
    return "Database metadata (table or column) is missing or invalid (NA)."
  if "does not exist" in error_msg.lower():
    return "Referenced database object does not exist."
  if "permission denied" in error_msg.lower():
    return "Permission denied to perform the database operation."

  return "An unknown database error occurred."


class BadRequest400(Exception):
  def __init__(self, message: str = 'Bad Request!', exc: Any = None):
    new_message = message
    if message.find('psycopg2') > -1:
      new_message = readable_db_error(message)
      if new_message == 'A database constraint was violated.':
        new_message += f' | {message}'
    self.name = new_message
    details = []
    if exc:
      try:
        tb = traceback.extract_tb(exc.__traceback__)
        for frame in tb:
          parts = frame.filename.strip("/").split("/")
          last_3_parts = parts[-3:]
          relative_path = "/".join(last_3_parts)
          details.append(f"{relative_path} {frame.name}, Line: {frame.lineno}, Code: {frame.line}")
      except: ''
    self.detail = details

class Unauthorized401(Exception):
  def __init__(self, message: str = 'Unauthorize!'):
    self.name = message
    # self.detail = str(Exception)

class Forbidden403(Exception):
  def __init__(self, message: str = 'Forbidden'):
    self.name = message

class NotFound404(Exception):
  def __init__(self, message: str | None = None, id: str | int | None = None):
    if message:
      self.name = message
    elif id:
      self.name = f'Data with id {id} not found'
    else:
      self.name = 'Data Not Found'

class RateLimit429(Exception):
  def __init__(self, message: str | None = None):
    if message:
      self.name = message
    else:
      self.name = 'The system is currently busy due to too many requests. Please try again later.'
