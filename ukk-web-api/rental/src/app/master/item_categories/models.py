import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime, String, Text


class ItemCategory(Base):
  __tablename__ = "item_categories"
  __table_args__ = {"schema": "rental"}
  __schema_app__ = "master"

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  name: Mapped[str] = mapped_column(String, nullable=False, index=True)
  description: Mapped[str | None] = mapped_column(Text, nullable=True)
  is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=True)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> Mapping[str, Mapped]:
  return {
    "id": ItemCategory.id,
    "name": ItemCategory.name,
    "description": ItemCategory.description,
    "is_active": ItemCategory.is_active,

    "created_by": ItemCategory.created_by,
    "updated_by": ItemCategory.updated_by,
    "created_at": ItemCategory.created_at,
    "updated_at": ItemCategory.updated_at,
    "deleted_at": ItemCategory.deleted_at,
    **custom_col
  }


class Req(BaseModel):
  name: str
  description: str | None = None
  is_active: bool | None = True