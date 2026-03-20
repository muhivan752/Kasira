"""global_event_log

Revision ID: 037
Revises: 036
Create Date: 2026-03-20 10:37:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '037'
down_revision = '036'
branch_labels = None
depends_on = None

def upgrade():
    # Create the partitioned table
    op.execute("""
        CREATE TABLE global_event_log (
            id UUID DEFAULT gen_random_uuid() NOT NULL,
            outlet_id UUID NOT NULL,
            event_type VARCHAR NOT NULL,
            payload JSONB,
            created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
            PRIMARY KEY (id, outlet_id)
        ) PARTITION BY HASH (outlet_id);
    """)

    # Create default partitions (e.g., 4 partitions for hash partitioning)
    op.execute("CREATE TABLE global_event_log_p0 PARTITION OF global_event_log FOR VALUES WITH (MODULUS 4, REMAINDER 0);")
    op.execute("CREATE TABLE global_event_log_p1 PARTITION OF global_event_log FOR VALUES WITH (MODULUS 4, REMAINDER 1);")
    op.execute("CREATE TABLE global_event_log_p2 PARTITION OF global_event_log FOR VALUES WITH (MODULUS 4, REMAINDER 2);")
    op.execute("CREATE TABLE global_event_log_p3 PARTITION OF global_event_log FOR VALUES WITH (MODULUS 4, REMAINDER 3);")

    # Create indexes on the partitioned table
    op.execute("CREATE INDEX ix_global_event_log_outlet_id ON global_event_log (outlet_id);")
    op.execute("CREATE INDEX ix_global_event_log_event_type ON global_event_log (event_type);")
    op.execute("CREATE INDEX ix_global_event_log_created_at ON global_event_log (created_at);")

def downgrade():
    op.execute("DROP TABLE global_event_log CASCADE;")
