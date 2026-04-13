
from app.auth.user.models import ConstAdditionalPermissions, User
from db.database import get_db
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from utils.helpers.hash import verify
from utils.responses import Unauthorized401

app = FastAPI()
security = HTTPBasic()

def basic_auth(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
  check_user = False
  user = db.query(User).filter(User.username == credentials.username, User.deleted_at.is_(None)).first()
  if not user:
    raise Unauthorized401('User not found')
  if user and user.additional_permissions and user.additional_permissions.find(ConstAdditionalPermissions.basic_auth) > -1:
    check_user = True
  if check_user is False:
    raise Unauthorized401('User not found')
  if not verify(user.password, credentials.password):
    raise Unauthorized401('Incorrect Password')
  # is_correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
  # is_correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)

  # if not (is_correct_username and is_correct_password):
  #     raise HTTPException(
  #         status_code=status.HTTP_401_UNAUTHORIZED,
  #         detail="Incorrect username or password",
  #         headers={"WWW-Authenticate": "Basic"},
  #     )
  return {
    'username': credentials.username,
    'companies': user.companies,
    'token': ''
  }