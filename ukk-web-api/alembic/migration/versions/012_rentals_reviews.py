"""012_rental_reviews

Revision ID: 012
Revises: 011
Create Date: 2026-03-30 00:00:00.000000

Review hanya bisa dibuat setelah rental berstatus 'selesai'.
Foto ulasan → auth.master_files
  module='rental_reviews', reference_id=reviews.id
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op

revision: str = '012'
down_revision: str | None = '011'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "reviews",
        sa.Column("id", sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("rental_id", sa.UUID, nullable=False, index=True),
        sa.Column("item_id", sa.BigInteger, nullable=False, index=True),
        sa.Column("customer_id", sa.BigInteger, nullable=False, index=True),
        sa.Column("rating", sa.SmallInteger, nullable=False),       # 1–5
        sa.Column("comment", sa.Text, nullable=True),
        sa.Column("is_visible", sa.Boolean, nullable=True, default=True),   # admin bisa hide

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, index=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["rental_id"], ["rental.rentals.id"], name="reviews_rental_id_fkey"),
        sa.ForeignKeyConstraint(["item_id"], ["rental.items.id"], name="reviews_item_id_fkey"),
        sa.ForeignKeyConstraint(["customer_id"], ["auth.users.id"], name="reviews_customer_id_fkey"),

        # 1 user hanya bisa review 1 item per rental
        sa.UniqueConstraint("rental_id", "item_id", "customer_id", name="uq_reviews_rental_item_customer"),
        schema="rental"
    )


def downgrade() -> None:
    op.drop_table("reviews", schema="rental")