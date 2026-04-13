"""015_rental_invoices

Revision ID: 015
Revises: 014
Create Date: 2026-04-02 00:00:00.000000

Invoice dibuat otomatis setelah payment.status berubah menjadi 'terverifikasi'.
Semua data di-snapshot agar invoice tidak berubah meski data induk berubah.

PDF hasil render disimpan di auth.master_files:
  module='rental_invoices', reference_id=invoices.id

Contoh invoice_code: INV-20260402-001
Contoh flow per rental:
  - Bayar sewa       → payment type='pembayaran'   → INV-20260402-001
  - Bayar denda      → payment type='denda'         → INV-20260402-002
  - Refund deposit   → payment type='refund_deposit'→ INV-20260402-003
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "015"
down_revision: str | None = "014"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "rental_invoices",
        sa.Column("id", sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),

        # Relasi ke tabel utama
        sa.Column("rental_id", sa.UUID, nullable=False, index=True),
        sa.Column("payment_id", sa.UUID, nullable=False, index=True),

        # Nomor invoice unik & berurutan
        sa.Column("invoice_code", sa.String, unique=True, nullable=False, index=True),

        # Tipe invoice mengikuti tipe payment:
        #   'pembayaran' | 'denda' | 'refund_deposit'
        sa.Column("type", sa.String, nullable=True, index=True),

        # ── Snapshot customer ──────────────────────────────────────────────
        sa.Column("customer_id", sa.BigInteger, nullable=True),
        sa.Column("customer_name", sa.String, nullable=True),
        sa.Column("customer_email", sa.String, nullable=True),
        sa.Column("customer_phone", sa.String, nullable=True),

        # ── Snapshot periode sewa ──────────────────────────────────────────
        sa.Column("rental_code", sa.String, nullable=True),
        sa.Column("start_date", sa.Date, nullable=True),
        sa.Column("end_date", sa.Date, nullable=True),
        sa.Column("duration_days", sa.Integer, nullable=True),

        # ── Snapshot rincian item ──────────────────────────────────────────
        # JSON array, contoh:
        # [
        #   {
        #     "item_id": 1, "item_code": "KMR-001", "item_name": "Kamera Sony A7III",
        #     "quantity": 1, "price_per_day": 150000, "duration_days": 3,
        #     "deposit_amount": 500000, "subtotal": 450000
        #   }
        # ]
        sa.Column("items_snapshot", JSONB, nullable=True),

        # ── Snapshot rincian biaya ─────────────────────────────────────────
        sa.Column("subtotal", sa.Float, nullable=True, default=0),
        sa.Column("deposit_total", sa.Float, nullable=True, default=0),
        sa.Column("fine_total", sa.Float, nullable=True, default=0),      # total denda jika ada
        sa.Column("grand_total", sa.Float, nullable=True, default=0),

        # ── Snapshot info pembayaran ───────────────────────────────────────
        sa.Column("payment_method", sa.String, nullable=True),            # transfer | cod
        sa.Column("bank_name", sa.String, nullable=True),
        sa.Column("account_number", sa.String, nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verified_by_name", sa.String, nullable=True),

        # ── PDF ────────────────────────────────────────────────────────────
        # Diisi setelah PDF selesai di-generate & disimpan ke auth.master_files
        sa.Column("pdf_file_id", sa.BigInteger, nullable=True),           # FK ke auth.master_files.id
        sa.Column("pdf_url", sa.String, nullable=True),

        # Status generate PDF: 'pending' | 'generated' | 'failed'
        sa.Column("pdf_status", sa.String, nullable=True, index=True, default="pending"),

        sa.Column("notes", sa.Text, nullable=True),

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),

        sa.ForeignKeyConstraint(["rental_id"], ["rental.rentals.id"], name="rental_invoices_rental_id_fkey"),
        sa.ForeignKeyConstraint(["payment_id"], ["rental.payments.id"], name="rental_invoices_payment_id_fkey"),

        # 1 payment hanya boleh menghasilkan 1 invoice
        sa.UniqueConstraint("payment_id", name="uq_rental_invoices_payment"),

        schema="rental",
    )


def downgrade() -> None:
    op.drop_table("rental_invoices", schema="rental")