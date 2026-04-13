import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import Boolean, ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, Float, String, Text


class Fine(Base):
  __tablename__ = "fines"
  __table_args__ = {"schema": "rental"}
  __schema_app__ = "transaction"

  id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
  rental_id: Mapped[str] = mapped_column(UUID, ForeignKey("rental.rentals.id"), nullable=False, index=True)
  created_by_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("auth.users.id"), nullable=True, index=True)
  type: Mapped[str | None] = mapped_column(String, nullable=True, index=True)  # keterlambatan | kerusakan | kehilangan
  amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)
  description: Mapped[str | None] = mapped_column(Text, nullable=True)
  is_paid: Mapped[bool | None] = mapped_column(Boolean, nullable=True, default=False)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
  updated_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> Mapping[str, Mapped]:
  return {
    "id": Fine.id,
    "rental_id": Fine.rental_id,
    "created_by_id": Fine.created_by_id,
    "type": Fine.type,
    "amount": Fine.amount,
    "description": Fine.description,
    "is_paid": Fine.is_paid,

    "created_by": Fine.created_by,
    "updated_by": Fine.updated_by,
    "created_at": Fine.created_at,
    "updated_at": Fine.updated_at,
    "deleted_at": Fine.deleted_at,
    **custom_col,
  }


class Req(BaseModel):
  rental_id: str
  type: str | None = None
  amount: float
  description: str | None = None
  is_paid: bool | None = False
