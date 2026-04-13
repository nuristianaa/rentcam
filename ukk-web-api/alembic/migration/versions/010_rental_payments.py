"""010_rental_payments

Revision ID: 010
Revises: 009
Create Date: 2026-03-15 00:00:00.000000

Foto bukti bayar → auth.master_files
  module='rental_payments', reference_id=payments.id
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = '010'
down_revision: str | None = '009'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column("id", sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("rental_id", sa.UUID, nullable=False, index=True),
        sa.Column("verified_by", sa.BigInteger, nullable=True, index=True),
        sa.Column("amount", sa.Float, nullable=False, default=0),
        sa.Column("type", sa.String, nullable=True, index=True),    # pembayaran | denda | refund_deposit
        sa.Column("status", sa.String, nullable=False, index=True), # menunggu | terverifikasi | ditolak
        sa.Column("bank_name", sa.String, nullable=True),
        sa.Column("account_number", sa.String, nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["rental_id"], ["rental.rentals.id"], name="payments_rental_id_fkey"),
        sa.ForeignKeyConstraint(["verified_by"], ["auth.users.id"], name="payments_verified_by_fkey"),
        schema="rental"
    )


def downgrade() -> None:
    op.drop_table("payments", schema="rental")