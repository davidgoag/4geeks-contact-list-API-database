"""empty message

Revision ID: a348910e8db7
Revises: e4707a1dd261
Create Date: 2021-11-20 00:01:46.409777

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a348910e8db7'
down_revision = 'e4707a1dd261'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('address', sa.String(length=220), nullable=True))
    op.drop_column('contact', 'adress')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contact', sa.Column('adress', mysql.VARCHAR(length=220), nullable=True))
    op.drop_column('contact', 'address')
    # ### end Alembic commands ###
