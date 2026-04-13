from typing import Any

from config.config import getenv, is_dev
from fastapi import Request
from fastapi.param_functions import Depends
from fastapi.security import HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from utils.responses import Forbidden403, RateLimit429, Unauthorized401

oauth2_scheme = HTTPBearer()

SECRET_KEY = getenv('JWT_SECRET', 'fbasjdk1o23i12nladskdn1p123mdasdj123ljasd13123lkn3123n1lk23n1k2j3n123132')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = int(getenv('JWT_EXPIRED_MINUTE', '30'))

#--------- GET USERNAME FROM JWT ---------#
def decode_token(creds = Depends(oauth2_scheme)):
  # Decode JWT
  token = creds.credentials
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  except JWTError:
    raise Unauthorized401()
  except Exception:
    raise Unauthorized401()
  # Return as Dictionary
  return {
    'token': token,
    'username': payload['sub'],
    'name': payload['name'],
    'user_id': payload.get('user_id'),
    'companies': payload.get('companies', ''),
    'vendors': payload.get('vendors', ''),
    'role_code': payload.get('role_code', ''),
    'additional_permissions': payload.get('additional_permissions', ''),
  }


#--------- GET CRED BASIC ---------#
def get_cred(request: Request, creds = Depends(oauth2_scheme)) -> dict[str, Any]:
  """
  Returns: dict{
    'token': 'eyxxx',
    'username': 'user',
    'name': 'user',
    companies: 'ABC,DEF',
    vendors: 'ABC,DEF',
    role_code: '',
    additional_permissions: 'ABC,DEF'
  }
  """

  # Check permission via API Gateway /check-permission
  if not is_dev():
    headers = request.headers
    if headers and headers.get('x-auth-message'):
      message = headers['x-auth-message']
      # print('x-auth-message: ', message)
      if message == 'Rate limit exceeded.':
        raise RateLimit429()
      if message.find('success') == -1:
        raise Forbidden403(message)

  return decode_token(creds)


#--------- GET CRED CUSTOM ACTION DEFINITION ---------#
def get_cred_with_permission(action: str = 'browse'):
  """
  Check based on parameter action. Return Forbidden if action is not exist in API Gateway.
  Returns: dict{
    'token': 'eyxxx',
    'username': 'user',
    'name': 'user',
    companies: 'ABC,DEF',
    vendors: 'ABC,DEF',
    role_code: '',
    additional_permissions: 'ABC,DEF'
  }
  """
  def _get_cred(
    request: Request,
    creds=Depends(oauth2_scheme),
  ):
    return exec_get_cred(request, action=action, creds=creds)
  return _get_cred

def exec_get_cred(request: Request, action: str, creds = Depends(oauth2_scheme)):
  # Check permission via API Gateway /check-permission
  if not is_dev():
    headers = request.headers
    if headers and headers.get('x-auth-message'):
      message = headers['x-auth-message']
      # print('x-auth-message: ', message)
      if message == 'Rate limit exceeded.':
        raise RateLimit429()

      # handle complex action strings
      if action.startswith("or:") or action.startswith("and:"):
        # parse allowed actions from message if present
        allowed_actions = [part.strip().lower() for part in message.replace("success ", "").split(", ")]
        allowed_actions = [a for a in allowed_actions if a]  # clean empties
        if not check_action_allowed(action, allowed_actions):
          msg = f"You do not have permission to perform {action}. {message}."
        raise Forbidden403(msg)

      if message.find(action) == -1:
        msg = f"You do not have permission to perform {action}. {message}."
        raise Forbidden403(msg)

  return decode_token(creds)


def check_action_allowed(action: str, allowed_actions: list[str]) -> bool:
  action = action.strip().lower()

  if action.startswith("or:"):
    parts = [p.strip() for p in action[3:].split(",")]
    return any(part in allowed_actions for part in parts)

  if action.startswith("and:"):
    parts = [p.strip() for p in action[4:].split(",")]
    return all(part in allowed_actions for part in parts)

  return action in allowed_actions