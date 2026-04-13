import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import BigInteger


class Permission(Base):
  __tablename__ = "permissions"
  __table_args__ = {"schema": "auth"}

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  app: Mapped[str] = mapped_column(nullable=True)
  name: Mapped[str] = mapped_column(nullable=True)
  created_by: Mapped[str] = mapped_column()
  updated_by: Mapped[str] = mapped_column()
  deleted_by: Mapped[str] = mapped_column()
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

  role_permissions = relationship("RolePermission", back_populates="permission")

  fillable = ["app", "name"]


def tbl_select() -> Mapping[str, Mapped]:
  return {
    "id": Permission.id,
    "app": Permission.app,
    "name": Permission.name,
    "created_by": Permission.created_by,
    "created_at": Permission.created_at,
    "updated_by": Permission.updated_by,
    "updated_at": Permission.updated_at,
    "deleted_by": Permission.deleted_by,
    "deleted_at": Permission.deleted_at,
  }


class Req(BaseModel):
  name: str | None = None
  app: str | None = None
