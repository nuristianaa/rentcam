"""008_rental_rentals

Revision ID: 008
Revises: 007
Create Date: 2026-03-15 00:00:00.000000

Status flow:
  menunggu_bayar → menunggu_verif → diproses → aktif → selesai
  (dari status apapun bisa → dibatalkan)
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = '008'
down_revision: str | None = '007'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "rentals",
        sa.Column("id", sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("rental_code", sa.String, unique=True, index=True, nullable=False),  # RF-20260315-001
        sa.Column("customer_id", sa.BigInteger, nullable=False, index=True),
        sa.Column("petugas_id", sa.BigInteger, nullable=True, index=True),
        sa.Column("start_date", sa.Date, nullable=False),
        sa.Column("end_date", sa.Date, nullable=False),
        sa.Column("duration_days", sa.Integer, nullable=True),
        sa.Column("subtotal", sa.Float, nullable=True, default=0),
        sa.Column("deposit_total", sa.Float, nullable=True, default=0),
        sa.Column("grand_total", sa.Float, nullable=True, default=0),
        sa.Column("payment_method", sa.String, nullable=True, index=True),             # transfer | cod
        sa.Column("status", sa.String, nullable=False, index=True),
        sa.Column("notes", sa.Text, nullable=True),

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["customer_id"], ["auth.users.id"], name="rentals_customer_id_fkey"),
        sa.ForeignKeyConstraint(["petugas_id"], ["auth.users.id"], name="rentals_petugas_id_fkey"),
        schema="rental"
    )


def downgrade() -> None:
    op.drop_table("rentals", schema="rental")