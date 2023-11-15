"""New Migration

Revision ID: 4dccfe6a5d41
Revises: ebfd17a6e56d
Create Date: 2023-09-17 00:19:48.336920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dccfe6a5d41'
down_revision = 'ebfd17a6e56d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'result',  # Replace with your table name
        'score',  # Replace with your column name
        type_=sa.Float(),  # Set the new data type to FLOAT
        existing_type=sa.Integer(),  # Set the existing data type to INTEGER
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        'result',
        'score',
        type_=sa.Integer(),  # Reverse the change by setting the data type back to INTEGER
        existing_type=sa.Float(),
    )
