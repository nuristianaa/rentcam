import datetime

from db.database import Base
from sqlalchemy import ForeignKey, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, DateTime, String, Text


class RentalHistory(Base):
  __tablename__ = "rental_histories"
  __table_args__ = {"schema": "rental"}

  id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
  rental_id: Mapped[str] = mapped_column(UUID, ForeignKey("rental.rentals.id"), nullable=False, index=True)

  # Nama event: status_changed | checkout | checkin | payment_submitted
  #             payment_verified | payment_rejected | fine_issued | rental_cancelled | review_submitted
  event: Mapped[str] = mapped_column(String, nullable=False, index=True)

  old_status: Mapped[str | None] = mapped_column(String, nullable=True)
  new_status: Mapped[str | None] = mapped_column(String, nullable=True)

  # Referensi opsional ke tabel lain
  payment_id: Mapped[str | None] = mapped_column(UUID, nullable=True, index=True)
  fine_id: Mapped[str | None] = mapped_column(UUID, nullable=True, index=True)
  review_id: Mapped[str | None] = mapped_column(UUID, nullable=True, index=True)

  # Konteks tambahan (snapshot, late_days, dll)
  data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

  actor: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
  actor_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("auth.users.id"), nullable=True, index=True)
  notes: Mapped[str | None] = mapped_column(Text, nullable=True)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), index=True)
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> dict:
  return {
    "id":         RentalHistory.id,
    "rental_id":  RentalHistory.rental_id,
    "event":      RentalHistory.event,
    "old_status": RentalHistory.old_status,
    "new_status": RentalHistory.new_status,
    "payment_id": RentalHistory.payment_id,
    "fine_id":    RentalHistory.fine_id,
    "review_id":  RentalHistory.review_id,
    "data":       RentalHistory.data,
    "actor":      RentalHistory.actor,
    "actor_id":   RentalHistory.actor_id,
    "notes":      RentalHistory.notes,
    "created_at": RentalHistory.created_at,
    **custom_col,
  }