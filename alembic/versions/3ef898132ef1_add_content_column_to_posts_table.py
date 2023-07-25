"""add content column to posts table

Revision ID: 3ef898132ef1
Revises: 30724e9505bb
Create Date: 2023-07-22 00:38:39.021970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ef898132ef1'
down_revision = '30724e9505bb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
