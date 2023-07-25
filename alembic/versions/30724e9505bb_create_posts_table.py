"""create posts table

Revision ID: 30724e9505bb
Revises: 
Create Date: 2023-07-22 00:03:16.459853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30724e9505bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
