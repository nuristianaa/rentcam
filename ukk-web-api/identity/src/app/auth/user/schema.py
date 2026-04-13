import re
from datetime import date

from pydantic import BaseModel, EmailStr
from utils.responses import BadRequest400

STRONG_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")


def validate_password(value: str):
  if not STRONG_PASSWORD_REGEX.match(value):
    raise BadRequest400("Password must be at least 8 characters long, include uppercase, lowercase, and digit.")
  return value


class UserCreate(BaseModel):
  email: EmailStr | None = None
  username: str | None = None
  name: str | None = None
  password: str | None = None
  phone: str | int | None = None
  title: str | None = None
  role_ids: list[int] | None = None
  additional_permissions: str | None = None
  location: str | None = None
  birthday: date | None = None
  profile_picture: str | None = None
  is_active: bool | None = None


class UserBase(BaseModel):
  name: str | None = None
  phone: str | int | None = None
  location: str | None = None
  country_code: str | None = None
  birthday: date | None = None
  table_configs: list | None = None
  table_summaries: list | None = None
  is_active: bool | None = None


class UserWithCred(UserBase):
  username: str | None = None
  email: EmailStr | None = None
  role_ids: list[int] | None = None
  title: str | None = None
  additional_permissions: str | None = None

  class Config:
    require_by_default = False


class FavMenu(BaseModel):
  menu_favorites: list | None = [{"id": 1, "app": "", "name": "test", "slug": "test", "path": "/test"}]


class ChangePass(BaseModel):
  current_password: str
  password: str


class ResetPass(BaseModel):
  password: str


class UserSign(BaseModel):
  signatures: str | None = None


class UserSignParams(BaseModel):
  email: str