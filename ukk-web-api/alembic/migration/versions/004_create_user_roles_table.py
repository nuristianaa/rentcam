"""004_create_user_roles_table

Revision ID: 004
Revises: 003
Create Date: 2025-08-06 22:09:51.565047

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "004"
down_revision: str | None = "003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
  op.create_table(
    "user_roles",
    sa.Column("user_id", sa.Integer(), sa.ForeignKey("auth.users.id", ondelete="CASCADE"), primary_key=True),
    sa.Column("role_id", sa.Integer(), sa.ForeignKey("auth.roles.id", ondelete="CASCADE"), primary_key=True),
    schema="auth",
  )


def downgrade():
  op.drop_table("user_roles", schema="auth")
