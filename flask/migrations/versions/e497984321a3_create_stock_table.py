"""create stock table

Revision ID: e497984321a3
Revises: 
Create Date: 2021-12-05 17:37:49.493267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e497984321a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'stocks',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('code', sa.String(20), nullable=False, index=True, unique=True),
        sa.Column('name', sa.String(20), nullable=False, index=True),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )
    op.create_table(
        'stocks_after_hour_information',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('stock_id', sa.Integer, nullable=False, index=True, unique=True),
        sa.ForeignKeyConstraint(['stock_id'], ['stocks.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.Column('max', sa.Float),
        sa.Column('min', sa.Float),
        sa.Column('open', sa.Float),
        sa.Column('close', sa.Float),
        sa.Column('spread', sa.Float),
        sa.Column('trading_volume', sa.String(100)),
        sa.Column('trading_money', sa.String(100)),
        sa.Column('trading_turnover', sa.String(100)),
        sa.Column('current_date', sa.Date),
    )

def downgrade():
    op.drop_table('stocks_after_hour_information')
    op.drop_table('stocks')
