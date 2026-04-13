import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel, field_validator
from sqlalchemy import ForeignKey, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime, SmallInteger, String, Text


class Review(Base):
  __tablename__ = "reviews"
  __table_args__ = (
    UniqueConstraint("rental_id", "item_id", "customer_id", name="uq_reviews_rental_item_customer"),
    {"schema": "rental"}
  )
  __schema_app__ = "transaction"

  id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
  rental_id: Mapped[str] = mapped_column(UUID, ForeignKey("rental.rentals.id"), nullable=False, index=True)
  item_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("rental.items.id"), nullable=False, index=True)
  customer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("auth.users.id"), nullable=False, index=True)
  rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)   # 1–5
  comment: Mapped[str | None] = mapped_column(Text, nullable=True)
  is_visible: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=True)  # admin bisa hide

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), index=True)
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> Mapping[str, Mapped]:
  return {
    "id": Review.id,
    "rental_id": Review.rental_id,
    "item_id": Review.item_id,
    "customer_id": Review.customer_id,
    "rating": Review.rating,
    "comment": Review.comment,
    "is_visible": Review.is_visible,

    "created_by": Review.created_by,
    "updated_by": Review.updated_by,
    "created_at": Review.created_at,
    "updated_at": Review.updated_at,
    "deleted_at": Review.deleted_at,
    **custom_col
  }


class Req(BaseModel):
  rental_id: str
  item_id: int
  rating: int
  comment: str | None = None

  @field_validator("rating")
  @classmethod
  def validate_rating(cls, v):
    if v < 1 or v > 5:
      raise ValueError("Rating harus antara 1 sampai 5.")
    return v


class ReqToggleVisible(BaseModel):
  is_visible: bool