import json
import time
from typing import Annotated, Any

from app.auth.oauth2 import (
  check_jwt,
  check_refresh_token,
  create_access_token,
  create_jwt_full,
  flatten_actions,
  get_username,
  query_check_permission,
)
from app.auth.role.models import Role
from app.auth.user.models import User
from app.auth.user_role.models import UserRole
from config import getenv
from db.database import get_async_db, get_async_db_log, get_db
from fastapi import APIRouter, Request
from fastapi.param_functions import Depends
from fastapi.responses import HTMLResponse, JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session
from utils.helpers.hash import bcrypt, verify
from utils.repo.services import service_api_email
from utils.responses import BadRequest400, Unauthorized401

from .helper import (
  LoginForm,
  ReqRefreshToken,
  translate_uri,
)

router = APIRouter(tags=["authentication"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/v1/token")
@limiter.limit("10/second")
async def get_token(
  request: Request,
  db: Annotated[AsyncSession, Depends(get_async_db)],
  db_log: Annotated[AsyncSession, Depends(get_async_db_log)],
  req: LoginForm = Depends(),
):
  # === Configuration ===
  JWT_EXPIRED_MINUTE = int(getenv("JWT_EXPIRED_MINUTE", "30"))
  expiry, device_id = JWT_EXPIRED_MINUTE, ""

  # === Validate user ===
  user = await get_user_auth(db=db, username=req.username)
  if not user                                : raise BadRequest400("Invalid credentials.")
  if not verify(user.password, req.password) : raise BadRequest400("Incorrect password.")

  # === Fetch roles ===
  role_codes_str = await get_role_codes_str(db=db, user_id=user.id)

  # === Create JWT ===
  try:
    data = create_jwt_full(user=user, expiry=expiry, device_id=device_id, role_codes=role_codes_str) # type: ignore
    return data
  except Exception as e:
    msg = str(e)
    raise BadRequest400(msg)


@router.post("/v1/refresh-token")
@limiter.limit("10/second")
async def refresh_token(
  request: Request,
  db: Annotated[AsyncSession, Depends(get_async_db)],
  req: ReqRefreshToken
) -> dict[str, Any]:
  # === Check & Get Username ===
  username = check_refresh_token(req.refresh_token)
  if not username: raise Unauthorized401()

  # === Validate user ===
  user = await get_user_auth(db=db, username=username)
  if not user: raise Unauthorized401()

  # === Fetch roles ===
  role_codes_str = await get_role_codes_str(db=db, user_id=user.id)

  try:
    expiry = int(getenv("JWT_EXPIRED_MINUTE", "30"))
    data = create_jwt_full(user=user, expiry=expiry, role_codes=role_codes_str) # type: ignore
    return data
  except Exception:
    raise Unauthorized401()


@router.get("/check-permission")
@limiter.limit("20/second")
async def check_permission(request: Request, db: Annotated[AsyncSession, Depends(get_async_db)]):
  """API gateway for check permission per module"""
  msg = ""
  headers: dict = request.headers  # type: ignore
  try: method: str = headers["x-original-method"]
  except: method = "GET"

  if method == "OPTIONS":
    return JSONResponse(status_code=200, content={"message": msg}, headers={"X-Auth-Message": "success"})

  try:
    username = get_username(headers)
    if username:
      uri = headers["x-original-uri"]
      app, prefix, action = translate_uri(method, uri)

      # === Special case for api error logs | Only SU can see ===
      if username == 'superuser' and prefix and prefix.find('api-error-logs') > -1:
        return JSONResponse(status_code=200, content={"message": msg}, headers={"X-Auth-Message": "success"})

      # === Fetch roles ===
      role_ids = select(UserRole.role_id).join(User, User.id == UserRole.user_id).where(User.username == username)
      role_ids = await db.execute(role_ids)
      role_ids = role_ids.all()
      role_ids = [r.role_id for r in role_ids]

      query = query_check_permission(role_ids, app, prefix)

      result = await db.execute(query)
      result = result.all()
      allowed_actions = flatten_actions(result)
      allowed_actions_str = ", ".join(sorted(allowed_actions))
      if len(allowed_actions) > 0:
        msg = f'You only have {allowed_actions_str} permission on {app} {prefix}'
      else:
        msg = f'You do not have any permission on {app} {prefix}'
      if action in allowed_actions:
        msg = f'success {allowed_actions_str}'
  except Exception as e:
    msg += "Exception: " + str(e)

  # Sanitize header value: remove newline/control characters
  def sanitize_header_value(value: str) -> str:
    if not value:
      return ""
    return "".join(c for c in value if 32 <= ord(c) <= 126)
  safe_header_msg = sanitize_header_value(msg)
  return JSONResponse(status_code=200, content={"message": msg}, headers={"X-Auth-Message": safe_header_msg})


@router.get("/v1/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)) -> dict[str, str]:
  try:
    expiry = 5  # minutes
    user = db.query(User.username).filter(User.email == email, User.deleted_at.is_(None)).first()
    if not user:
      raise BadRequest400("Invalid credentials")
    url = getenv("PUBLIC_MAIN", "http://localhost:8090")
    expires = int(round(time.time() * 1000)) + expiry * 60000
    subdata = {"sub": user.username, "exp": expires}
    access_token = create_access_token(data=subdata)

    link = f"{url}/v1/reset-password?p={access_token}"
    body = f"<p>Please click the link to reset your password:</p><p><a href='{link}'>{link}</a></p><p>This link is valid for 5 minutes.</p>"
    email = service_api_email(to=[email], subject="Forgot Password", body=body)
    if str(email).find("success") > -1:
      return {"message": f"sending email, please check your inbox, reset password only valid for {expiry} minutes."}
    else:
      raise BadRequest400("sending email failed " + email)
  except Exception as e:
    msg = "Auth Forgot Password exception: " + str(e)
    raise BadRequest400(msg)


@router.get("/v1/reset-password", response_class=HTMLResponse)
async def req_reset_password(p: str | None, password: str | None = None, db: Session = Depends(get_db)):
  scheme = 0
  username = None
  if p:
    username = check_jwt(p)
  if username:
    user = db.query(User).filter(User.username == username, User.deleted_at.is_(None)).first()
    if user:
      scheme = 1
      if password:
        try:
          new_password = bcrypt(password)
          db.query(User).filter(User.username == username, User.deleted_at.is_(None)).update(
            {User.password: new_password}
          )
          db.commit()
          scheme = 2
        except:
          db.rollback()
          scheme = 0
  
  # Return HTML response based on scheme
  if scheme == 0:
    html = "<h1>Link Expired!</h1>"
  elif scheme == 2:
    html = "<h1>Your password has been changed successfully!</h1>"
  else:
    html = f"""<form action="" method="get" name="signupForm" id="signupForm">
      <h2 class="formTitle">Create new password</h2>
      <div class="inputDiv">
        <label class="inputLabel" for="password">New Password</label>
        <input type="password" id="password" name="password" required>
      </div>
      <div class="inputDiv">
        <label class="inputLabel" for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" name="confirmPassword">
      </div>
      <div style="display:none;">
        <input type="text" id="p" name="p" value="{p}">
      </div>
      <div class="buttonWrapper">
        <button type="submit" id="submitButton" onclick="validateSignupForm()" class="submitButton pure-button pure-button-primary">
          <span>Continue</span>
          <span id="loader"></span>
        </button>
      </div>
    </form>"""
  return html


@router.get("/client")
async def check_client(request: Request):
  try:
    client = json.dumps(request.client)  # IP CLIENT
    user_agent = request.headers.get("user-agent", "Unknown")
    return {"message": "success", "client": client, "user_agent": user_agent}
  except Exception as e:
    msg = "check_client failed: " + str(e)
    raise BadRequest400(msg)


#---------- HELPERS ---------#
async def get_user_auth(db: AsyncSession, username: str):
  try:
    # === Fetch roles ===
    s_user = select(
      User.id,
      User.password,
      User.username,
      User.name,
      User.email,
      User.additional_permissions,
      User.is_active
    ).where(or_(User.username == username, User.email == username, User.phone == username), User.deleted_at.is_(None))
    r_user = await db.execute(s_user)
    return r_user.first()
  except Exception as e:
    print('get_user_auth: ', e)
    return None

async def get_role_codes_str(db: Annotated, user_id: int|str):
  try:
    # === Fetch roles ===
    role_stmt = select(Role.name).join(UserRole, Role.id == UserRole.role_id).where(UserRole.user_id == user_id)
    result = await db.execute(role_stmt)
    role_codes = result.scalars().all()
    if not role_codes: raise BadRequest400("User has not been assigned to any role. Please contact the administrator")
    role_codes_str = ",".join(role_codes) if role_codes else "" # type: ignore
    return role_codes_str
  except Exception:
    return ""
