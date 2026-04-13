"""018_add_missing_columns_to_users

Revision ID: 018
Revises: 017
Create Date: 2026-04-13 10:10:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "018"
down_revision: str | None = "017"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
  op.add_column("users", sa.Column("profile_picture", sa.String, nullable=True), schema="auth")
  op.add_column("users", sa.Column("storage_id", sa.String, nullable=True), schema="auth")
  op.add_column("users", sa.Column("vendors", sa.String, nullable=True), schema="auth")
  op.add_column("users", sa.Column("signatures", sa.JSON, nullable=True), schema="auth")
  op.add_column("users", sa.Column("storage_signatures", sa.JSON, nullable=True), schema="auth")


def downgrade():
  op.drop_column("users", "profile_picture", schema="auth")
  op.drop_column("users", "storage_id", schema="auth")
  op.drop_column("users", "vendors", schema="auth")
  op.drop_column("users", "signatures", schema="auth")
  op.drop_column("users", "storage_signatures", schema="auth")
