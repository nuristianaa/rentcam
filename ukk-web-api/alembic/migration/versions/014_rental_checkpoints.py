"""014_rental_checkpoints

Revision ID: 014
Revises: 013
Create Date: 2026-04-02 00:00:00.000000

Mencatat kondisi alat saat keluar (checkout) dan saat kembali (checkin).

Foto kondisi alat → auth.master_files
  module='rental_checkpoints', reference_id=checkpoints.id

Alur:
  1. Petugas klik "Serahkan Alat" → insert row type='checkout'
     → rental status berubah 'diproses' → 'aktif'
     → catat waktu actual_at, kondisi, checklist, foto

  2. Customer bawa balik → petugas klik "Terima Alat" → insert row type='checkin'
     → rental status berubah 'aktif' → 'selesai'
     → catat waktu actual_at, kondisi, kerusakan (jika ada)
     → jika actual_at > rentals.end_date → sistem bisa auto-buat fine keterlambatan
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "014"
down_revision: str | None = "013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "rental_checkpoints",
        sa.Column("id", sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("rental_id", sa.UUID, nullable=False, index=True),

        # 'checkout' = alat keluar ke customer
        # 'checkin'  = alat kembali dari customer
        sa.Column("type", sa.String, nullable=False, index=True),

        # Waktu actual serah terima (bisa beda dari start_date / end_date yang direncanakan)
        sa.Column("actual_at", sa.DateTime(timezone=True), nullable=False, index=True),

        # Kondisi umum alat: 'baik' | 'cacat_ringan' | 'rusak' | 'hilang'
        sa.Column("condition", sa.String, nullable=True, index=True),

        # Deskripsi bebas kondisi alat (misal: "ada goresan di body kanan")
        sa.Column("condition_notes", sa.Text, nullable=True),

        # Checklist poin-poin kelengkapan/kondisi dalam format JSON array
        # Contoh: [{"label": "Lensa", "ok": true}, {"label": "Tas", "ok": false, "note": "tali putus"}]
        sa.Column("checklist", JSONB, nullable=True),

        # Petugas yang melakukan serah terima
        sa.Column("officer_id", sa.BigInteger, nullable=True, index=True),
        sa.Column("officer_name", sa.String, nullable=True),

        # Tanda tangan digital customer (path / base64 / url)
        sa.Column("customer_signature", sa.String, nullable=True),

        # Catatan tambahan dari petugas
        sa.Column("notes", sa.Text, nullable=True),

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),

        sa.ForeignKeyConstraint(["rental_id"], ["rental.rentals.id"], name="rental_checkpoints_rental_id_fkey"),
        sa.ForeignKeyConstraint(["officer_id"], ["auth.users.id"], name="rental_checkpoints_officer_id_fkey"),

        # Satu rental hanya boleh punya 1 checkout dan 1 checkin
        sa.UniqueConstraint("rental_id", "type", name="uq_rental_checkpoints_rental_type"),

        schema="rental",
    )


def downgrade() -> None:
    op.drop_table("rental_checkpoints", schema="rental")