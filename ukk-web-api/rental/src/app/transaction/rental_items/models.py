import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, Float, Integer, String


class RentalItem(Base):
  __tablename__ = "rental_items"
  __table_args__ = {"schema": "rental"}
  __schema_app__ = "transaction"

  id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
  rental_id: Mapped[str] = mapped_column(UUID, ForeignKey("rental.rentals.id"), nullable=False, index=True)
  item_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("rental.items.id"), nullable=False, index=True)
  quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
  price_per_day: Mapped[float] = mapped_column(Float, nullable=False)      # snapshot saat order
  deposit_amount: Mapped[float | None] = mapped_column(Float, nullable=True)  # snapshot saat order
  subtotal: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> Mapping[str, Mapped]:
  return {
    "id": RentalItem.id,
    "rental_id": RentalItem.rental_id,
    "item_id": RentalItem.item_id,
    "quantity": RentalItem.quantity,
    "price_per_day": RentalItem.price_per_day,
    "deposit_amount": RentalItem.deposit_amount,
    "subtotal": RentalItem.subtotal,

    "created_by": RentalItem.created_by,
    "created_at": RentalItem.created_at,
    "updated_at": RentalItem.updated_at,
    "deleted_at": RentalItem.deleted_at,
    **custom_col
  }