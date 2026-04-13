import datetime
from collections.abc import Mapping

from db.database import Base
from pydantic import BaseModel, field_validator
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import BigInteger, Date, DateTime, Float, Integer, String, Text
from app.auth.user.models import User


class Rental(Base):
  __tablename__ = "rentals"
  __table_args__ = {"schema": "rental"}
  __schema_app__ = "transaction"

  id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True, server_default=text("gen_random_uuid()"))
  rental_code: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
  customer_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("auth.users.id"), nullable=False, index=True)
  petugas_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("auth.users.id"), nullable=True, index=True)
  start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
  end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
  duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
  subtotal: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)
  deposit_total: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)
  grand_total: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)
  payment_method: Mapped[str | None] = mapped_column(String, nullable=True, index=True)  # transfer | cod
  status: Mapped[str] = mapped_column(String, nullable=False, index=True)
  # menunggu_bayar | menunggu_verif | diproses | aktif | selesai | dibatalkan
  notes: Mapped[str | None] = mapped_column(Text, nullable=True)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), index=True)
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

  # Explicit foreign_keys untuk menghindari ambiguity karena ada 2 FK ke auth.users
  customer = relationship(
    "User",
    foreign_keys=[customer_id],
    primaryjoin="Rental.customer_id == User.id"
  )
  petugas = relationship(
    "User",
    foreign_keys=[petugas_id],
    primaryjoin="Rental.petugas_id == User.id"
  )


def tbl_select(custom_col: dict = {}) -> Mapping[str, Mapped]:
  return {
    "id": Rental.id,
    "rental_code": Rental.rental_code,
    "customer_id": Rental.customer_id,
    "petugas_id": Rental.petugas_id,
    "start_date": Rental.start_date,
    "end_date": Rental.end_date,
    "duration_days": Rental.duration_days,
    "subtotal": Rental.subtotal,
    "deposit_total": Rental.deposit_total,
    "grand_total": Rental.grand_total,
    "payment_method": Rental.payment_method,
    "status": Rental.status,
    "notes": Rental.notes,

    "created_by": Rental.created_by,
    "updated_by": Rental.updated_by,
    "created_at": Rental.created_at,
    "updated_at": Rental.updated_at,
    "deleted_at": Rental.deleted_at,
    **custom_col
  }


# ─────────────────────────────────────────────────────────────────────────────
# Request schemas
# ─────────────────────────────────────────────────────────────────────────────

class ReqItem(BaseModel):
  item_id: int
  quantity: int = 1


class Req(BaseModel):
  customer_id: int
  start_date: datetime.date
  end_date: datetime.date
  payment_method: str           # transfer | cod
  notes: str | None = None
  items: list[ReqItem]          # list alat yang disewa

class ReqUpdate(BaseModel):
  customer_id: int
  petugas_id: int | None = None
  start_date: datetime.date
  end_date: datetime.date
  payment_method: str
  notes: str | None = None
  items: list[ReqItem]
  status: str | None = None


class ReqUpdateStatus(BaseModel):
  status: str
  petugas_id: int | None = None
  notes: str | None = None


class ReqCheckpoint(BaseModel):
  """
  Dipakai untuk endpoint checkout maupun checkin.
  `type` diisi otomatis oleh service, tidak perlu dikirim dari client.
  """
  officer_id: int | None = None
  condition: str | None = None  # baik | cacat_ringan | rusak | hilang
  condition_notes: str | None = None
  checklist: list[dict] | None = None
  # Contoh checklist:
  # [{"label": "Lensa", "ok": true}, {"label": "Tas", "ok": false, "note": "tali putus"}]
  customer_signature: str | None = None
  notes: str | None = None

  @field_validator("condition")
  @classmethod
  def validate_condition(cls, v):
    valid = {"baik", "cacat_ringan", "rusak", "hilang"}
    if v and v not in valid:
      raise ValueError(f"Kondisi tidak valid. Pilihan: {', '.join(valid)}")
    return v