"""016_role_permissions

Revision ID: 016
Revises: 015
Create Date: 2026-04-13 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "016"
down_revision: str | None = "015"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
  op.create_table(
    "roles_permissions",
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("role_id", sa.BigInteger, sa.ForeignKey("auth.roles.id"), nullable=True),
    sa.Column("permission_id", sa.BigInteger, sa.ForeignKey("auth.permissions.id"), nullable=True),
    sa.Column("browse", sa.Boolean, default=False),
    sa.Column("create", sa.Boolean, default=False),
    sa.Column("read", sa.Boolean, default=False),
    sa.Column("update", sa.Boolean, default=False),
    sa.Column("delete", sa.Boolean, default=False),
    sa.Column("restore", sa.Boolean, default=False),
    sa.Column("others", sa.JSON, nullable=True),
    sa.Column("created_by", sa.String, nullable=True),
    sa.Column("updated_by", sa.String, nullable=True),
    sa.Column("deleted_by", sa.String, nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    schema="auth",
  )


def downgrade():
  op.drop_table("roles_permissions", schema="auth")
