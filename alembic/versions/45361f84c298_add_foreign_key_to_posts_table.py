"""add foreign-key to posts table

Revision ID: 45361f84c298
Revises: c710e3794abe
Create Date: 2023-07-23 19:31:56.906552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45361f84c298'
down_revision = 'c710e3794abe'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
