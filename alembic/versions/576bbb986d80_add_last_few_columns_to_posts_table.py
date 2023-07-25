"""add last few columns to posts table

Revision ID: 576bbb986d80
Revises: 45361f84c298
Create Date: 2023-07-24 23:00:50.642045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '576bbb986d80'
down_revision = '45361f84c298'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('publisched', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts', 'publisched')
    op.drop_column('posts', 'created_at')
    pass
