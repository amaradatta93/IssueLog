"""fk to username from issues

Revision ID: 25459163afbb
Revises: 1dcea938abb8
Create Date: 2020-06-12 18:13:46.119110

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '25459163afbb'
down_revision = '1dcea938abb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('issues', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_constraint('issues_ibfk_1', 'issues', type_='foreignkey')
    op.create_foreign_key(None, 'issues', 'user', ['user_id'], ['username'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'issues', type_='foreignkey')
    op.create_foreign_key('issues_ibfk_1', 'issues', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.alter_column('issues', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###
