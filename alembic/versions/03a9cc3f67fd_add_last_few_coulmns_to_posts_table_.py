"""add last few coulmns to posts table(swear to God:))

Revision ID: 03a9cc3f67fd
Revises: 8e02b572f2ac
Create Date: 2022-09-02 08:25:45.642034

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03a9cc3f67fd'
down_revision = '8e02b572f2ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
