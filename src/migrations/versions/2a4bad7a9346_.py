"""empty message

Revision ID: 2a4bad7a9346
Revises: d8124a07ad27
Create Date: 2024-09-18 23:09:50.484388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a4bad7a9346'
down_revision = 'd8124a07ad27'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('rooms',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hotel_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('rooms')
