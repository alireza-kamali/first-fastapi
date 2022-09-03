"""create posts table

Revision ID: c0df2ac7a910
Revises: 
Create Date: 2022-09-01 04:30:24.190188

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0df2ac7a910'        # to implement these changes with alembic upgrade we have to provide revision number.

down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():        # this is for when we wanted to drop a table.we can roll back.
    op.drop_table('posts')
    pass
