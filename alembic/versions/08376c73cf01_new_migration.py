"""New Migration

Revision ID: 08376c73cf01
Revises: 4dccfe6a5d41
Create Date: 2023-09-17 03:14:09.285726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08376c73cf01'
down_revision = '4dccfe6a5d41'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('result', sa.Column('topic_name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('result', 'topic_name')
    # ### end Alembic commands ###
