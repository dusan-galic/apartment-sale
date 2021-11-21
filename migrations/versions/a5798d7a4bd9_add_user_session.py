"""add user session

Revision ID: a5798d7a4bd9
Revises: 197e55772a77
Create Date: 2021-11-02 15:12:20.801067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5798d7a4bd9'
down_revision = '197e55772a77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tbl_user_sessions',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ip_of_login', sa.Text(), nullable=False),
    sa.Column('session_token', sa.Text(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_of_creation', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('date_of_update', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), server_default=sa.text('false'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tbl_user_sessions')
    # ### end Alembic commands ###
