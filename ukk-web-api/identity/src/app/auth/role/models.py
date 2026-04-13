import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import JSON, BigInteger, Boolean, DateTime, String


class Role(Base):
  __tablename__ = "roles"
  __table_args__ = {"schema": "auth"}

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  name: Mapped[str | None] = mapped_column(String, unique=True, nullable=False)

  created_by: Mapped[str | None] = mapped_column(String(), nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String(), nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String(), nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

  users = relationship("User", secondary="auth.user_roles", back_populates="roles")
  role_permissions = relationship("RolePermission", back_populates="role")


class RolePermission(Base):
  __tablename__ = "roles_permissions"
  __table_args__ = {"schema": "auth"}

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("auth.roles.id"), nullable=True)
  permission_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("auth.permissions.id"), nullable=True)
  browse: Mapped[bool] = mapped_column(Boolean, default=False)
  create: Mapped[bool] = mapped_column(Boolean, default=False)
  read: Mapped[bool] = mapped_column(Boolean, default=False)
  update: Mapped[bool] = mapped_column(Boolean, default=False)
  delete: Mapped[bool] = mapped_column(Boolean, default=False)
  restore: Mapped[bool] = mapped_column(Boolean, default=False)
  others: Mapped[list|dict|None] = mapped_column(JSON, nullable=True)

  created_by: Mapped[str | None] = mapped_column(String(), nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String(), nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String(), nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)

  role = relationship("Role", back_populates="role_permissions")
  permission = relationship("Permission", back_populates="role_permissions")



def tbl_select() -> Mapping[str, Mapped]:
  return {
    "id": Role.id,
    "name": Role.name,
    "created_at": Role.created_at,
    "updated_at": Role.updated_at,
    "deleted_at": Role.deleted_at,
  }


class ReqPermissions(BaseModel):
  id: str|int|None = None
  app: str|int|None = None
  name: str|int|None = None
  detail: dict|None = None

class Req(BaseModel):
  name: str
  permissions: list[ReqPermissions]|None = None

class RoleReq(BaseModel):
  name: str|None = None
  permissions: str|None = None
  browse: bool|None = False
  create: bool|None = False
  read: bool|None = False
  update: bool|None = False
  delete: bool|None = False
  restore: bool|None = False
  others: list|dict|None = None

class PermissionReq(BaseModel):
  app: str
  permission: str
  no: int

class InsertReqBulk(BaseModel):
  bulk: bool = False
  roles: list[RoleReq] = []
  permissions: list[PermissionReq] = []
