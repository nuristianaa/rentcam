import math
import time
import uuid
from typing import Any, Literal, LiteralString

from app.auth.helper import translate_uri2
from app.auth.permission.models import Permission
from app.auth.role.models import RolePermission
from app.auth.user.models import User
from app.auth.user_role.models import UserRole
from config import getenv
from cryptography.fernet import Fernet
from db.database import get_db
from fastapi import Request
from fastapi.param_functions import Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from utils.responses import Forbidden403, Unauthorized401

TOKEN_SCHEMA = getenv("TOKEN_SCHEMA", "password")

oauth2_scheme = HTTPBearer() if TOKEN_SCHEMA == "token" else OAuth2PasswordBearer(tokenUrl="v1/token")

SECRET_KEY = getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = int(getenv("JWT_EXPIRED_MINUTE", "30"))
JWT_REFRESH_EXPIRED_HOUR = float(getenv("JWT_REFRESH_EXPIRED_HOUR", "8"))
# FERNET_KEY = Fernet.generate_key()  # Save and reuse this securely
# print(FERNET_KEY.decode())
FERNET_KEY = getenv("FERNET_KEY")
fernet = Fernet(FERNET_KEY.encode())


def create_jwt_full(*, user: User, expiry: int, device_id: str | None = None, role_codes: str|None = None) -> dict[str, Any]:
  """
  Extract and return claims from a JWT.

  Args:
      creds (str): Encoded JWT from OAuth2 dependency.

  Returns:
      Dict[str, Any]: A dictionary containing JWT claims such as:
          - 'sub' (str): The subject (username).
          - 'user_id' (str): The user ID.
          - 'username' (str): The username.
          - 'email' (str): The email.
          - 'name' (str): The name.
          - 'companies' (str): Companies.
          - 'role_code' (str): Role codes.
          - 'additional_permissions' (str): Additional permissions for the user, comma separated.
          - 'utc' (int): Current timestamp in milliseconds.
          - 'exp' (int): Expiration timestamp.
          - 'device_id' (str): Device ID (Optional).
  """
  token_id = str(uuid.uuid4())  # Random unique string
  currentms = int(round(time.time() * 1000))
  expires = currentms + expiry * 60000
  encrypted_data = fernet.encrypt(f"{token_id}|{expires}".encode()).decode()
  to_encode = {
    "ed": encrypted_data,
    "sub": user.username,
    "user_id": user.id,
    "username": user.username,
    "name": user.name,
    "email": user.email,
    "role_code": role_codes,
    "additional_permissions": user.additional_permissions,
    "utc": currentms,
    "exp": expires,
    "device_id": device_id,
  }
  access_token = create_access_token(to_encode)

  refresh_expires = currentms + int(JWT_REFRESH_EXPIRED_HOUR * 60 * 60 * 1000)
  refresh_encrypted = fernet.encrypt(f"{user.username}|{refresh_expires}".encode()).decode()
  refresh_token = create_access_token({'en': refresh_encrypted})
  return {
    "token_type": "bearer",
    "access_token": access_token,
    "refresh_token": refresh_token,
    "expire_token": expires,
    **to_encode
  }


def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


def check_jwt(token: str) -> str | Literal[False]:
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload["sub"]
    if username is None or username == "":
      return False
    currentms = int(round(time.time() * 1000))
    exp = payload["exp"]
    if exp < currentms:
      return False
    return username
  except JWTError:
    return False


########## GET USERNAME FROM JWT ##########
def get_username(headers: dict):
  try:
    # access_token: str = headers['x-access-token']
    # if (check_access_token(access_token) == False): return None
    auth: str = headers["authorization"]
    token = auth[7:]
    username = check_jwt(token)
    return username
  except Exception as e:
    print(e)
    return None


def get_cred(request: Request, creds=Depends(oauth2_scheme)) -> dict[str, Any]:
  """
  Extract and return claims from a JWT.

  Args:
      creds (str): Encoded JWT from OAuth2 dependency.

  Returns:
      Dict[str, Any]: A dictionary containing JWT claims such as:
          - 'ed' (str): Encrypted expired date so there is no eternal token.
          - 'sub' (str): The subject (username).
          - 'user_id' (str): The user ID.
          - 'username' (str): The username.
          - 'email' (str): The email.
          - 'name' (str): The name.
          - 'companies' (str): List companies.
          - 'vendors' (str): List vendors.
          - 'role_code' (str): Role code.
          - 'additional_permissions' (str): Additional permissions for the user, comma separated.
          - 'utc' (int): Current timestamp in milliseconds.
          - 'exp' (int): Expiration timestamp.
          - 'device_id' (str): Device ID (Optional).
  """
  if TOKEN_SCHEMA == "token":
    token: str = creds.credentials
  else:
    token: str = creds
  # Decode JWT
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    currentms = int(round(time.time() * 1000))
    username = payload["sub"]
    encrypted = payload["ed"]
    decrypted = fernet.decrypt(encrypted.encode()).decode()
    token_id, exp = decrypted.split("|")
    exp = int(exp)
    print('Exp JWT: ',  exp, currentms)
    if exp < currentms:
      raise Unauthorized401()
  except JWTError as e:
    print(e)
    raise Unauthorized401()
  except Exception as e:
    print(e)
    raise Unauthorized401()

  # Return as Dictionary
  return {
    "token": token,
    "username": username,
    "name": payload.get("name", ""),
    "email": payload.get("email", ""),
    "role_code": payload.get("role_code", ""),
    "additional_permissions": payload.get("additional_permissions", ""),
  }


def get_cred_base(creds=Depends(oauth2_scheme)) -> dict[str, str]:
  if TOKEN_SCHEMA == "token":
    token: str = creds.credentials
  else:
    token: str = creds
  # Decode JWT
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload["sub"]
    name: str = payload["name"]
  except JWTError as e:
    print(e)
    raise Unauthorized401()
  except Exception as e:
    print(e)
    raise Unauthorized401()

  # Return as Dictionary
  return {
    "token": token,
    "username": username,
    "name": name,
    "companies": payload.get("companies", ""),
    "vendors": payload.get("vendors", ""),
    "role_code": payload.get("role_code", ""),
    "additional_permissions": payload.get("additional_permissions", ""),
  }


def check_refresh_token(token: str):
  """
  Extract and return claims from a JWT.
  """
  username = None
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    currentms = int(round(time.time() * 1000))
    encrypted = payload["en"]
    decrypted = fernet.decrypt(encrypted.encode()).decode()
    username, exp = decrypted.split("|")
    exp = int(exp)
    if exp < currentms:
      raise Unauthorized401()
  except JWTError as e:
    print(e)
    raise Unauthorized401()
  except Exception as e:
    print(e)
    raise Unauthorized401()
  return username


########## CHECK MODULE PERMISSION ##########
def check_permission(cred: dict, db: Session = Depends(get_db), module: str | None = None) -> Literal[True]:
  # forbidden = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to do this", headers={"WWW-Authenticate": "Bearer"})
  username = cred.get("username")
  if module is None:
    raise Forbidden403

  try:
    # user = db.query(User.role_id).filter(User.username == username).first()
    role_ids = (
      db.query(UserRole.role_id)
        .join(User, User.id == UserRole.user_id)
        .filter(User.username == username)
        .all()
    )

    role_ids = [r[0] for r in role_ids]
    if not role_ids:
      raise Forbidden403

    if len(role_ids) > 0:
      prefix = "module"
      action = "browse"
      mods = ["browse", "read", "create", "update", "delete", "restore"]
      for m in mods:
        if module.find(m) > -1:
          prefix = module.replace(f"-{m}", "")
          action = m

    role_ids_str = ", ".join(map(str, role_ids))
    query = f"""
        SELECT bool_or(rp.{action}) AS has_permission
        FROM auth.roles_permissions rp
        LEFT JOIN auth.permissions p ON p.id = rp.permission_id
        WHERE rp.role_id IN ({role_ids_str})
          AND p.name ILIKE :prefix
    """

    result = db.execute(text(query), {"prefix": f"%{prefix}%"}).scalar()
    # result = result.scalars().first()

    if result:
      return True

    raise Forbidden403
  except Exception as e:
    raise Forbidden403(str(e))


########## GET DATA FROM JWT ##########
def get_cred_with_permission(action: str):
  def _get_cred(
    request: Request,
    db: Session = Depends(get_db),
    creds=Depends(oauth2_scheme),
  ):
    return exec_get_cred(request, db=db, action=action, creds=creds)
  return _get_cred

def exec_get_cred(
  request: Request,
  creds=Depends(oauth2_scheme),
  db: Session|None = None,
  action: str|None = None
) -> dict[str, Any]:
  """
  Extract and return claims from a JWT.

  Args:
    creds (str): Encoded JWT from OAuth2 dependency.

  Returns:
    Dict[str, Any]: A dictionary containing JWT claims such as:
      - 'ed' (str): Encrypted expired date so there is no eternal token.
      - 'sub' (str): The subject (username).
      - 'user_id' (str): The user ID.
      - 'username' (str): The username.
      - 'email' (str): The email.
      - 'name' (str): The name.
      - 'companies' (str): List companies.
      - 'vendors' (str): List vendors.
      - 'role_code' (str): Role code.
      - 'additional_permissions' (str): Additional permissions for the user, comma separated.
      - 'utc' (int): Current timestamp in milliseconds.
      - 'exp' (int): Expiration timestamp.
      - 'device_id' (str): Device ID (Optional).
  """
  if TOKEN_SCHEMA == "token":
    token: str = creds.credentials
  else:
    token: str = creds

  # 1. Decode JWT
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    currentms = int(round(time.time() * 1000))
    username = payload["sub"]
    encrypted = payload["ed"]
    decrypted = fernet.decrypt(encrypted.encode()).decode()
    _token_id, exp = decrypted.split("|")
    exp = int(exp)
    # print('Exp JWT: ',  exp, currentms)
    if exp < currentms:
      raise Unauthorized401()
  except JWTError as e:
    print(e)
    raise Unauthorized401()
  except Exception as e:
    print(e)
    raise Unauthorized401()

  # 2. Check Permission
  if db and action:
    exec_check_permission(request=request, username=username, db=db, action=action)
  # Return as Dictionary
  return {
    "token": token,
    "username": username,
    "name": payload.get("name", ""),
    "email": payload.get("email", ""),
    "role_code": payload.get("role_code", ""),
    "additional_permissions": payload.get("additional_permissions", ""),
  }

def exec_check_permission(request: Request, username: str, db: Session, action: str):
  action = action.strip().lower()
  uri = request.url.path
  try:
    headers: dict = request.headers  # type: ignore
    uri = headers["x-original-uri"]
  except:
    ''
  app, prefix = translate_uri2(uri)
  if prefix is None:
    raise Forbidden403

  try:
    role_ids = db.query(UserRole.role_id).join(User, User.id == UserRole.user_id).where(User.username == username).all()
    role_ids = [r[0] for r in role_ids]
    if not role_ids:
      raise Forbidden403

    query_permission = query_check_permission(role_ids, app, prefix)
    result = db.execute(query_permission).all()
    allowed_actions = flatten_actions(result) # Flatten results into a set of allowed actions

    # OR logic: at least one must be allowed
    if action.startswith("or:"):
        parts = action[3:].split(",")
        return any(part in allowed_actions for part in parts)

    # AND logic: all must be allowed
    if action.startswith("and:"):
        parts = action[4:].split(",")
        return all(part in allowed_actions for part in parts)

    # Default: single action check
    if action in allowed_actions: return True

    raise Forbidden403(f'You do not have permission to {action} {app} {prefix}.')
  except Exception as e:
    raise Forbidden403(str(e))

def query_check_permission(role_ids: list[str], app: str, prefix: str):
  return (
    select(
      RolePermission.browse,
      RolePermission.read,
      RolePermission.create,
      RolePermission.update,
      RolePermission.delete,
      RolePermission.restore,
      RolePermission.others
    )
    .join(Permission, Permission.id == RolePermission.permission_id, isouter=True)
    .where(RolePermission.role_id.in_(role_ids), Permission.app == app, Permission.name.ilike(f'{prefix}%'))
  )

def flatten_actions(result):
  allowed_actions = set()
  for row in result:
    if getattr(row, "browse", None):
      allowed_actions.add("browse")
    if getattr(row, "read", None):
      allowed_actions.add("read")
    if getattr(row, "create", None):
      allowed_actions.add("create")
    if getattr(row, "update", None):
      allowed_actions.add("update")
    if getattr(row, "delete", None):
      allowed_actions.add("delete")
    if getattr(row, "restore", None):
      allowed_actions.add("restore")
    if row.others:
      allowed_actions.update(row.others)
  return allowed_actions


########## CUSTOM X-ACCESS-TOKEN ##########
def check_access_token(token: str) -> bool:
  now = gen_access_token()
  return token == now


def gen_access_token() -> LiteralString | Literal[""]:
  result = ""
  timemillis = int(round(time.time() * 1000))
  day = 60000 * 24  # valid for one day
  num = round(timemillis / day) * 7777777
  characters = "Aa0Bb1Cc2Dd3Ee4Ff5Gg6Hh7Ii8Jj9KkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
  charactersLength = 62
  lists = [int(i) for i in str(num)]
  # arrlen = len(lst)
  i = 0
  for el in lists:
    iter = (el + i) * num
    print(iter)
    key = int(str(iter)[-2:])
    to = math.floor(key / 99 * charactersLength)
    fr = to - 1
    result += characters[fr:to]
    i += 1
  return result
