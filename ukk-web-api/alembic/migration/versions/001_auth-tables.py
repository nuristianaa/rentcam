"""001_auth-tables

Revision ID: 001
Create Date: 2023-11-23 09:25:16.892591

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("create schema auth")

    op.create_table(
        'permissions',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('app', sa.String, nullable=True, index=True),
        sa.Column('name', sa.String, nullable=False, index=True),
        sa.Column('created_by', sa.String, nullable=True),
        sa.Column('updated_by', sa.String, nullable=True),
        sa.Column('deleted_by', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        schema='auth'
    )
    op.create_table(
        'roles',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('created_by', sa.String, nullable=True),
        sa.Column('updated_by', sa.String, nullable=True),
        sa.Column('deleted_by', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        schema='auth'
    )


    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('username', sa.String, unique=True, index=True, nullable=False),
        sa.Column('email', sa.String, unique=True, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False, index=True),
        sa.Column('phone', sa.String, nullable=True),
        sa.Column('title', sa.String, nullable=True),
        sa.Column('is_active', sa.Boolean, nullable=True, default=True),

        sa.Column('notifications', sa.String, nullable=True),

        sa.Column('location', sa.String, nullable=True),
        sa.Column('country_code', sa.String, nullable=True),
        sa.Column('birthday', sa.Date, nullable=True),

        sa.Column('created_by', sa.String, nullable=True),
        sa.Column('updated_by', sa.String, nullable=True),
        sa.Column('deleted_by', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        schema='auth'
    )

    op.create_table(
        "notifications",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("username", sa.String, nullable=True, index=True),
        sa.Column("user_id", sa.BigInteger, nullable=True),
        sa.Column("is_read", sa.Boolean, default=False, index=True),
        sa.Column("app", sa.String, nullable=True),
        sa.Column("title", sa.String, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("path", sa.String, nullable=True),
        sa.Column("type", sa.String, nullable=True),
        sa.Column("color", sa.String, nullable=True),
        sa.Column("icon", sa.String, nullable=True),

        sa.Column("created_by", sa.String, nullable=True),
        sa.Column("updated_by", sa.String, nullable=True),
        sa.Column("deleted_by", sa.String, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["auth.users.id"], name="auth_notifications_user_id_fkey"),
        schema="auth"
    )

    op.create_table(
        "master_files",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("app", sa.String, nullable=True, index=True),
        sa.Column("name", sa.String, nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("filename", sa.String, nullable=True),
        sa.Column("path", sa.String, nullable=True),
        sa.Column("module", sa.String, nullable=True, index=True),
        sa.Column("reference_code", sa.String, nullable=True, index=True),
        sa.Column("reference_id", sa.String, nullable=True, index=True),

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
    op.drop_table('permissions', schema='auth')
    op.drop_table('notifications', schema='auth')
    op.drop_table('users', schema='auth')
    op.drop_table('roles', schema='auth')
    op.drop_table('master_files', schema='auth')
    op.execute("drop schema auth")
