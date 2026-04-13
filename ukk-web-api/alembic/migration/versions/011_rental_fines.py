"""011_rental_fines

Revision ID: 011
Revises: 010
Create Date: 2026-03-15 00:00:00.000000

Foto bukti kerusakan → auth.master_files
  module='rental_fines', reference_id=fines.id
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = '011'
down_revision: str | None = '010'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "fines",
        sa.Column("id", sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("rental_id", sa.UUID, nullable=False, index=True),
        sa.Column("created_by_id", sa.BigInteger, nullable=True, index=True),
        sa.Column("type", sa.String, nullable=True, index=True),    # keterlambatan | kerusakan | kehilangan
        sa.Column("amount", sa.Float, nullable=False, default=0),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("is_paid", sa.Boolean, nullable=True, default=False),

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["rental_id"], ["rental.rentals.id"], name="fines_rental_id_fkey"),
        sa.ForeignKeyConstraint(["created_by_id"], ["auth.users.id"], name="fines_created_by_id_fkey"),
        schema="rental"
    )


def downgrade() -> None:
    op.drop_table("fines", schema="rental")