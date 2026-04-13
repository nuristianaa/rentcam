"""017_add_additional_permissions_to_users

Revision ID: 017
Revises: 016
Create Date: 2026-04-13 10:05:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "017"
down_revision: str | None = "016"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
  op.add_column("users", sa.Column("additional_permissions", sa.String, nullable=True), schema="auth")


def downgrade():
  op.drop_column("users", "additional_permissions", schema="auth")
