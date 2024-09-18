"""empty message

Revision ID: d8124a07ad27
Revises:
Create Date: 2024-09-18 22:42:18.222876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8124a07ad27'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('hotels')
