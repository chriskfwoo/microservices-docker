"""empty message

Revision ID: 107c2881c7ba
Revises: 
Create Date: 2018-08-19 19:19:17.366363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '107c2881c7ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
