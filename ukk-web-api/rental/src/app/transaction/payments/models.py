import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, Float, String, Text


class Payment(Base):
  __tablename__ = "payments"
  __table_args__ = {"schema": "rental"}
  __schema_app__ = "transaction"

  id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
  rental_id: Mapped[str] = mapped_column(UUID, ForeignKey("rental.rentals.id"), nullable=False, index=True)
  verified_by: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("auth.users.id"), nullable=True, index=True)
  amount: Mapped[float] = mapped_column(Float, nullable=False, default=0)
  type: Mapped[str | None] = mapped_column(String, nullable=True, index=True)   # pembayaran | denda | refund_deposit
  status: Mapped[str] = mapped_column(String, nullable=False, index=True)       # menunggu | terverifikasi | ditolak
  bank_name: Mapped[str | None] = mapped_column(String, nullable=True)
  account_number: Mapped[str | None] = mapped_column(String, nullable=True)
  notes: Mapped[str | None] = mapped_column(Text, nullable=True)
  paid_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  verified_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), index=True)
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> Mapping[str, Mapped]:
  return {
    "id": Payment.id,
    "rental_id": Payment.rental_id,
    "verified_by": Payment.verified_by,
    "amount": Payment.amount,
    "type": Payment.type,
    "status": Payment.status,
    "bank_name": Payment.bank_name,
    "account_number": Payment.account_number,
    "notes": Payment.notes,
    "paid_at": Payment.paid_at,
    "verified_at": Payment.verified_at,

    "created_by": Payment.created_by,
    "updated_by": Payment.updated_by,
    "created_at": Payment.created_at,
    "updated_at": Payment.updated_at,
    "deleted_at": Payment.deleted_at,
    **custom_col
  }


class Req(BaseModel):
  rental_id: str
  amount: float
  type: str                           # pembayaran | denda | refund_deposit
  status: str | None = None           # menunggu | terverifikasi | ditolak
  bank_name: str | None = None
  account_number: str | None = None
  notes: str | None = None
  paid_at: datetime.datetime | None = None


class ReqVerify(BaseModel):
  status: str                         # terverifikasi | ditolak
  notes: str | None = None