"""add users table

Revision ID: 88bfb88eccd0
Revises: 5d99667cb426
Create Date: 2022-09-01 07:20:31.022050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88bfb88eccd0'
down_revision = '5d99667cb426'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
