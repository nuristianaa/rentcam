import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime, Float, Integer, String, Text


class Item(Base):
  __tablename__ = "items"
  __table_args__ = {"schema": "rental"}
  __schema_app__ = "master"

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
  category_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("rental.item_categories.id"), nullable=True, index=True)
  code: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
  name: Mapped[str] = mapped_column(String, nullable=False, index=True)
  brand: Mapped[str | None] = mapped_column(String, nullable=True)
  description: Mapped[str | None] = mapped_column(Text, nullable=True)
  condition: Mapped[str | None] = mapped_column(String, nullable=True)        # baik | rusak_ringan
  stock_total: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
  stock_available: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
  price_per_day: Mapped[float] = mapped_column(Float, nullable=False, default=0)
  deposit_amount: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)
  is_active: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=True)
  images: Mapped[list | None] = mapped_column(JSONB, nullable=True)           # foto alat

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> Mapping[str, Mapped]:
  return {
    "id": Item.id,
    "category_id": Item.category_id,
    "code": Item.code,
    "name": Item.name,
    "brand": Item.brand,
    "description": Item.description,
    "condition": Item.condition,
    "stock_total": Item.stock_total,
    "stock_available": Item.stock_available,
    "price_per_day": Item.price_per_day,
    "deposit_amount": Item.deposit_amount,
    "is_active": Item.is_active,
    "images": Item.images,

    "created_by": Item.created_by,
    "updated_by": Item.updated_by,
    "created_at": Item.created_at,
    "updated_at": Item.updated_at,
    "deleted_at": Item.deleted_at,
    **custom_col
  }


class Req(BaseModel):
  category_id: int | None = None
  code: str
  name: str
  brand: str | None = None
  description: str | None = None
  condition: str | None = None
  stock_total: int | None = 0
  stock_available: int | None = 0
  price_per_day: float
  deposit_amount: float | None = 0
  is_active: bool | None = True
  images: list | dict | None = None