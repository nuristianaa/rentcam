"""013_rental_histories

Revision ID: 013
Revises: 012
Create Date: 2026-04-02 00:00:00.000000

Mencatat setiap perubahan status dan aktivitas penting pada sebuah rental.

Contoh penggunaan:
  - status berubah dari 'menunggu_bayar' → 'menunggu_verif'
  - pembayaran diterima / ditolak
  - denda dibuat
  - alat dikembalikan

Kolom `data` (JSONB) menyimpan snapshot konteks saat event terjadi,
misal: { "old_status": "aktif", "new_status": "selesai", "payment_id": "..." }
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "013"
down_revision: str | None = "012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "rental_histories",
        sa.Column("id", sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("rental_id", sa.UUID, nullable=False, index=True),

        # Event yang terjadi, contoh nilai:
        #   status_changed | payment_submitted | payment_verified | payment_rejected
        #   fine_issued | item_returned | rental_cancelled | review_submitted
        sa.Column("event", sa.String, nullable=False, index=True),

        # Status rental sebelum dan sesudah event (nullable, hanya diisi jika event mengubah status)
        sa.Column("old_status", sa.String, nullable=True),
        sa.Column("new_status", sa.String, nullable=True),

        # Referensi opsional ke tabel lain yang memicu event ini
        sa.Column("payment_id", sa.UUID, nullable=True, index=True),
        sa.Column("fine_id", sa.UUID, nullable=True, index=True),
        sa.Column("review_id", sa.UUID, nullable=True, index=True),

        # Data konteks tambahan dalam format JSON
        sa.Column("data", JSONB, nullable=True),

        # Siapa yang memicu event
        sa.Column("actor", sa.String, nullable=True, index=True),       # username
        sa.Column("actor_id", sa.BigInteger, nullable=True, index=True),
        sa.Column("notes", sa.Text, nullable=True),

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),

        sa.ForeignKeyConstraint(["rental_id"], ["rental.rentals.id"], name="rental_histories_rental_id_fkey"),
        sa.ForeignKeyConstraint(["actor_id"], ["auth.users.id"], name="rental_histories_actor_id_fkey"),

        schema="rental",
    )


def downgrade() -> None:
    op.drop_table("rental_histories", schema="rental")