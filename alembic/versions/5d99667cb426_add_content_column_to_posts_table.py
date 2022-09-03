"""add content column to posts table

Revision ID: 5d99667cb426
Revises: c0df2ac7a910
Create Date: 2022-09-01 06:16:03.652196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d99667cb426'
down_revision = 'c0df2ac7a910'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass
# note that everytime you define an upgrade function you should define the downgrade .
# alembic heads is a command we run in Terminal and that is gonna show us the latest change we apply and to upgrade we can use revision or head statement.
# if for any reason we wanted to undo these changes we use oposite commands:alembic downgrade c0df2ac7a910 or we can say alembic revision -1 .by this command we can go to one revision back.


def downgrade():
    op.drop_column("posts", "content")        # in this case we have to pass the name of the table we wanna drop and that specific column.
    pass
