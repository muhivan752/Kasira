"""subscription_payments

Revision ID: 048
Revises: 047
Create Date: 2026-03-20 10:48:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '048'
down_revision = '047'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'subscription_payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), primary_key=True),
        sa.Column('subscription_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('subscriptions.id', ondelete='CASCADE'), nullable=False),
        sa.Column('invoice_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('invoices.id', ondelete='SET NULL'), nullable=True),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('payment_method', sa.String(), nullable=False), # e.g., 'credit_card', 'bank_transfer'
        sa.Column('reference_id', sa.String(), nullable=True),
        sa.Column('status', sa.String(), server_default='success', nullable=False), # e.g., 'success', 'failed'
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    )

def downgrade():
    op.drop_table('subscription_payments')
