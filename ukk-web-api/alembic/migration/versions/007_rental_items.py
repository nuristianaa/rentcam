"""007_rental_items

Revision ID: 007
Revises: 006
Create Date: 2026-03-15 00:00:00.000000

Foto alat disimpan sebagai JSON array di kolom images (pola seperti NCR Reporting).
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = '007'
down_revision: str | None = '006'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "items",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("category_id", sa.BigInteger, nullable=True, index=True),
        sa.Column("code", sa.String, unique=True, index=True, nullable=False),
        sa.Column("name", sa.String, nullable=False, index=True),
        sa.Column("brand", sa.String, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("condition", sa.String, nullable=True),
        sa.Column("stock_total", sa.Integer, nullable=True, default=0),
        sa.Column("stock_available", sa.Integer, nullable=True, default=0),
        sa.Column("price_per_day", sa.Float, nullable=False, default=0),
        sa.Column("deposit_amount", sa.Float, nullable=True, default=0),
        sa.Column("is_active", sa.Boolean, nullable=True, default=True),
        sa.Column("images", JSONB, nullable=True),                  # foto alat (JSON array)

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["rental.item_categories.id"], name="items_category_id_fkey"),
        schema="rental"
    )


def downgrade() -> None:
    op.drop_table("items", schema="rental")