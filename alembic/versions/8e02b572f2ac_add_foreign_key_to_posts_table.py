"""add foreign_key to posts table

Revision ID: 8e02b572f2ac
Revises: 88bfb88eccd0
Create Date: 2022-09-02 08:00:20.516881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e02b572f2ac'
down_revision = '88bfb88eccd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=["owner_id"],
                          remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
