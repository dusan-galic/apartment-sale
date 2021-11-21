"""add broj_stana

Revision ID: 1bbc1c8e2121
Revises: 31781fb89265
Create Date: 2021-11-16 15:00:26.307410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bbc1c8e2121'
down_revision = '31781fb89265'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_stan', sa.Column('broj_stana', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tbl_stan', 'broj_stana')
    # ### end Alembic commands ###