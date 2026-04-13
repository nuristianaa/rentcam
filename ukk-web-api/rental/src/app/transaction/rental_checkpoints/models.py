import datetime
from typing import Any

from db.database import Base
from pydantic import BaseModel
from sqlalchemy import ForeignKey, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, String, Text


# ─────────────────────────────────────────
# Pydantic — Request Schemas
# ─────────────────────────────────────────

class ReqItem(BaseModel):
  item_id: int
  quantity: int


class Req(BaseModel):
  customer_id: int
  start_date: datetime.date
  end_date: datetime.date
  payment_method: str
  items: list[ReqItem]
  notes: str | None = None


class ReqUpdateStatus(BaseModel):
  status: str
  petugas_id: int | None = None
  notes: str | None = None


class ReqCheckpoint(BaseModel):
  condition: str | None = None          # 'baik' | 'cacat_ringan' | 'rusak' | 'hilang'
  condition_notes: str | None = None
  checklist: list[Any] | None = None   # [{"label": "Lensa", "ok": true, "note": "..."}, ...]
  officer_id: int | None = None
  customer_signature: str | None = None
  notes: str | None = None


# ─────────────────────────────────────────
# SQLAlchemy — Table Model
# ─────────────────────────────────────────

class RentalCheckpoint(Base):
  __tablename__ = "rental_checkpoints"
  __table_args__ = (
    UniqueConstraint("rental_id", "type", name="uq_rental_checkpoints_rental_type"),
    {"schema": "rental"},
  )

  id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
  rental_id: Mapped[str] = mapped_column(UUID, ForeignKey("rental.rentals.id"), nullable=False, index=True)

  # 'checkout' | 'checkin'
  type: Mapped[str] = mapped_column(String, nullable=False, index=True)

  actual_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

  # 'baik' | 'cacat_ringan' | 'rusak' | 'hilang'
  condition: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
  condition_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

  # [{"label": "Lensa", "ok": true}, {"label": "Tas", "ok": false, "note": "tali putus"}]
  checklist: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

  officer_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("auth.users.id"), nullable=True, index=True)
  officer_name: Mapped[str | None] = mapped_column(String, nullable=True)
  customer_signature: Mapped[str | None] = mapped_column(String, nullable=True)
  notes: Mapped[str | None] = mapped_column(Text, nullable=True)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), index=True)
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> dict:
  return {
    "id":                 RentalCheckpoint.id,
    "rental_id":          RentalCheckpoint.rental_id,
    "type":               RentalCheckpoint.type,
    "actual_at":          RentalCheckpoint.actual_at,
    "condition":          RentalCheckpoint.condition,
    "condition_notes":    RentalCheckpoint.condition_notes,
    "checklist":          RentalCheckpoint.checklist,
    "officer_id":         RentalCheckpoint.officer_id,
    "officer_name":       RentalCheckpoint.officer_name,
    "customer_signature": RentalCheckpoint.customer_signature,
    "notes":              RentalCheckpoint.notes,
    "created_at":         RentalCheckpoint.created_at,
    **custom_col,
  }