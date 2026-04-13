from datetime import datetime
from enum import Enum
from typing import Annotated

from db.database import Base
from fastapi import Form
from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, deferred, mapped_column, relationship
from sqlalchemy.sql.sqltypes import JSON, BigInteger, Boolean, String


class User(Base):
  __tablename__ = "users"
  __table_args__ = {"schema": "auth"}

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
  password: Mapped[str] = deferred(mapped_column(String, nullable=False))
  name: Mapped[str] = mapped_column(String, nullable=False)
  phone: Mapped[str | None] = mapped_column(String, nullable=True)
  title: Mapped[str | None] = mapped_column(String, nullable=True)
  additional_permissions: Mapped[str | None] = mapped_column(String, nullable=True)
  notifications: Mapped[str | None] = mapped_column(String, nullable=True)

  location: Mapped[str | None] = mapped_column(String, nullable=True)
  country_code: Mapped[str | None] = mapped_column(String, nullable=True)
  birthday: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

  profile_picture: Mapped[str | None] = mapped_column(String, nullable=True)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
  updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

  roles = relationship("Role", secondary="auth.user_roles", back_populates="users")
  is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True)


class FileReq:
  def __init__(
    self,
    *,
    ids: Annotated[str|None, Form()] = None,
  ):
    self.ids = ids


class ConstAdditionalPermissions:
  basic_auth: str = "basic_auth"
  receive_all_chats: str = "receive_all_chats"
  allow_cancel_approval: str = "allow_cancel_approval"
  # two: str = 'two'


class ConstType(str, Enum):
  additional_permissions = "additional_permissions"
  # notifications = "notifications"
  # tracker_group = "tracker_group"
  # role_code = "role_code"
  # companies = "companies"


# class ConstRoleCode:
#   superuser: str = "superuser"
#   admin: str = "admin"
#   vendor: str = "vendor"

# class ConstNotifications:
#   monitor_lc_skbdn: str = "monitor_lc_skbdn"
