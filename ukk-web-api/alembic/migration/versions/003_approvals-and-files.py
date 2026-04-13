"""005_approvals

Revision ID: 005
Create Date: 2025-05-08 11:75:00

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: str | None = '002'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
  op.execute("create schema transaction")

  op.drop_table("master_files", schema="auth")
  op.create_table(
    "master_files",
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("app", sa.String, nullable=True, index=True),
    sa.Column("name", sa.String, nullable=True),
    sa.Column("description", sa.Text, nullable=True),
    sa.Column("filename", sa.String, nullable=True),
    sa.Column("filetype", sa.String, nullable=True),
    sa.Column("path", sa.String, nullable=True),
    sa.Column("module", sa.String, nullable=True, index=True),
    sa.Column("reference_code", sa.String, nullable=True, index=True),
    sa.Column("reference_id", sa.String, nullable=True, index=True),
    sa.Column("is_public", sa.Boolean, nullable=True),
    sa.Column("storage_id", sa.String, nullable=True),
    sa.Column("base_url", sa.String, nullable=True),

    sa.Column("created_by", sa.String, nullable=True),
    sa.Column("updated_by", sa.String, nullable=True),
    sa.Column("deleted_by", sa.String, nullable=True),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    # sa.ForeignKeyConstraint(["role_id"], ["auth.roles.id"], name="role_user_id_fkey"),
    schema="auth"
  )

def downgrade() -> None:
  op.execute("drop schema transaction")
