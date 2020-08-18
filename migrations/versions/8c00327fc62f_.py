"""empty message

Revision ID: 8c00327fc62f
Revises: 34fb501946ae
Create Date: 2020-08-18 12:35:09.289706

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8c00327fc62f'
down_revision = '34fb501946ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('issues', 'issue_fix_date',
               existing_type=mysql.VARCHAR(length=10),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('issues', 'issue_fix_date',
               existing_type=mysql.VARCHAR(length=10),
               nullable=False)
    # ### end Alembic commands ###
