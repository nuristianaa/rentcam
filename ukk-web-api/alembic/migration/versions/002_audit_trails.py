"""002_audit_trails

Revision ID: 001
Create Date: 2025-06-09 09:25:16.892591

"""
import datetime
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: str | None = '001'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # Create parent table
    op.execute("""
        CREATE TABLE audit_trails (
            id UUID NOT NULL DEFAULT gen_random_uuid(),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            type VARCHAR,
            app VARCHAR,
            name VARCHAR,
            schema VARCHAR,
            module VARCHAR,
            module_id VARCHAR,
            username VARCHAR,
            data JSONB,
            PRIMARY KEY (id, created_at)
        ) PARTITION BY RANGE (created_at);
    """)

    start = datetime.date(2025, 1, 1)
    end = datetime.date(2036, 1, 1)  # 11 years = 132 partitions

    current = start
    while current < end:
        next_month = (current.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
        suffix = current.strftime('%Y_%m')
        op.execute(f"""
            CREATE TABLE audit_trails_{suffix} PARTITION OF audit_trails
            FOR VALUES FROM ('{current}') TO ('{next_month}');
        """)
        for col in ['type', 'app', 'name', 'schema', 'module', 'module_id', 'username']:
            op.create_index(f'ix_audit_trails_{suffix}_{col}', f'audit_trails_{suffix}', [col])
        current = next_month


def downgrade() -> None:
    start = datetime.date(2025, 1, 1)
    end = datetime.date(2036, 1, 1)
    current = start
    while current < end:
        suffix = current.strftime('%Y_%m')
        op.execute(f"DROP TABLE IF EXISTS audit_trails_{suffix}")
        current = (current.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    op.execute("DROP TABLE IF EXISTS audit_trails")
