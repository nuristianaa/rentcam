"""009_rental_rental_items

Revision ID: 009
Revises: 008
Create Date: 2026-03-15 00:00:00.000000

Harga & deposit di-snapshot saat order dibuat.
Perubahan harga item di masa depan tidak mempengaruhi histori order.
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = '009'
down_revision: str | None = '008'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "rental_items",
        sa.Column("id", sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("rental_id", sa.UUID, nullable=False, index=True),
        sa.Column("item_id", sa.BigInteger, nullable=False, index=True),
        sa.Column("quantity", sa.Integer, nullable=False, default=1),
        sa.Column("price_per_day", sa.Float, nullable=False),       # snapshot saat order
        sa.Column("deposit_amount", sa.Float, nullable=True),       # snapshot saat order
        sa.Column("subtotal", sa.Float, nullable=True, default=0),  # price_per_day x qty x duration_days

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["rental_id"], ["rental.rentals.id"], name="rental_items_rental_id_fkey"),
        sa.ForeignKeyConstraint(["item_id"], ["rental.items.id"], name="rental_items_item_id_fkey"),
        schema="rental"
    )


def downgrade() -> None:
    op.drop_table("rental_items", schema="rental")