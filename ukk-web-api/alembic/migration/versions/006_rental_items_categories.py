"""006_rental_item_categories

Revision ID: 006
Revises: 005
Create Date: 2026-03-15 00:00:00.000000
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = '006'
down_revision: str | None = '005'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "item_categories",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("name", sa.String, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=True, default=True),

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        schema="rental"
    )


def downgrade() -> None:
    op.drop_table("item_categories", schema="rental")