"""005_rental_schema

Revision ID: 005
Revises: 004
Create Date: 2026-03-15 00:00:00.000000
"""
from collections.abc import Sequence
from alembic import op

revision: str = '005'
down_revision: str | None = '004'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS rental")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS rental CASCADE")