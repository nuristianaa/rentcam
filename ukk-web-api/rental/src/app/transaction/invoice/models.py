import datetime

from db.database import Base
from sqlalchemy import ForeignKey, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BigInteger, Date, DateTime, Float, Integer, String, Text


class RentalInvoice(Base):
  __tablename__ = "rental_invoices"
  __table_args__ = (
    UniqueConstraint("payment_id", name="uq_rental_invoices_payment"),
    {"schema": "rental"},
  )

  id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
  rental_id: Mapped[str] = mapped_column(UUID, ForeignKey("rental.rentals.id"), nullable=False, index=True)
  payment_id: Mapped[str] = mapped_column(UUID, ForeignKey("rental.payments.id"), nullable=False, index=True)

  invoice_code: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

  # pembayaran | denda | refund_deposit
  type: Mapped[str | None] = mapped_column(String, nullable=True, index=True)

  # Snapshot customer
  customer_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
  customer_name: Mapped[str | None] = mapped_column(String, nullable=True)
  customer_email: Mapped[str | None] = mapped_column(String, nullable=True)
  customer_phone: Mapped[str | None] = mapped_column(String, nullable=True)

  # Snapshot periode sewa
  rental_code: Mapped[str | None] = mapped_column(String, nullable=True)
  start_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
  end_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
  duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True)

  # Snapshot item — JSON array
  # [{"item_id": 1, "item_code": "KMR-001", "item_name": "Kamera Sony A7III",
  #   "quantity": 1, "price_per_day": 150000, "duration_days": 3,
  #   "deposit_amount": 500000, "subtotal": 450000}]
  items_snapshot: Mapped[list | None] = mapped_column(JSONB, nullable=True)

  # Snapshot rincian biaya
  subtotal: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)
  deposit_total: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)
  fine_total: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)
  grand_total: Mapped[float | None] = mapped_column(Float, nullable=True, default=0)

  # Snapshot info pembayaran
  payment_method: Mapped[str | None] = mapped_column(String, nullable=True)
  bank_name: Mapped[str | None] = mapped_column(String, nullable=True)
  account_number: Mapped[str | None] = mapped_column(String, nullable=True)
  paid_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  verified_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
  verified_by_name: Mapped[str | None] = mapped_column(String, nullable=True)

  # PDF
  pdf_file_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
  pdf_url: Mapped[str | None] = mapped_column(String, nullable=True)
  # pending | generated | failed
  pdf_status: Mapped[str | None] = mapped_column(String, nullable=True, index=True, default="pending")

  notes: Mapped[str | None] = mapped_column(Text, nullable=True)

  created_by: Mapped[str | None] = mapped_column(String, nullable=True)
  updated_by: Mapped[str | None] = mapped_column(String, nullable=True)
  deleted_by: Mapped[str | None] = mapped_column(String, nullable=True)
  created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), index=True)
  updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
  deleted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


def tbl_select(custom_col: dict = {}) -> dict:
  return {
    "id":               RentalInvoice.id,
    "rental_id":        RentalInvoice.rental_id,
    "payment_id":       RentalInvoice.payment_id,
    "invoice_code":     RentalInvoice.invoice_code,
    "type":             RentalInvoice.type,
    "customer_id":      RentalInvoice.customer_id,
    "customer_name":    RentalInvoice.customer_name,
    "rental_code":      RentalInvoice.rental_code,
    "start_date":       RentalInvoice.start_date,
    "end_date":         RentalInvoice.end_date,
    "duration_days":    RentalInvoice.duration_days,
    "subtotal":         RentalInvoice.subtotal,
    "deposit_total":    RentalInvoice.deposit_total,
    "fine_total":       RentalInvoice.fine_total,
    "grand_total":      RentalInvoice.grand_total,
    "payment_method":   RentalInvoice.payment_method,
    "paid_at":          RentalInvoice.paid_at,
    "verified_at":      RentalInvoice.verified_at,
    "pdf_status":       RentalInvoice.pdf_status,
    "pdf_url":          RentalInvoice.pdf_url,
    "created_at":       RentalInvoice.created_at,
    **custom_col,
  }