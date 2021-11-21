"""is validated

Revision ID: d5312c5e3e81
Revises: a5798d7a4bd9
Create Date: 2021-11-03 12:42:18.852072

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd5312c5e3e81'
down_revision = 'a5798d7a4bd9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tbl_potencijlani_kupac', sa.Column('is_validated', sa.Boolean(), server_default=sa.text('false'), nullable=True))
    op.add_column('tbl_potencijlani_kupac', sa.Column('validated_by', sa.Integer(), nullable=True))
    op.alter_column('tbl_potencijlani_kupac', 'broj_ugovora',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
    op.alter_column('tbl_potencijlani_kupac', 'datum_ugovora',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.create_foreign_key(None, 'tbl_potencijlani_kupac', 'tbl_user', ['validated_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tbl_potencijlani_kupac', type_='foreignkey')
    op.alter_column('tbl_potencijlani_kupac', 'datum_ugovora',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('tbl_potencijlani_kupac', 'broj_ugovora',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)
    op.drop_column('tbl_potencijlani_kupac', 'validated_by')
    op.drop_column('tbl_potencijlani_kupac', 'is_validated')
    # ### end Alembic commands ###