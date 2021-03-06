"""empty message

Revision ID: 48d97d2acb8c
Revises: 9bca7e6c37fb
Create Date: 2022-04-10 19:55:43.706720

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48d97d2acb8c'
down_revision = '9bca7e6c37fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'comment', 'user', ['author'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comment', 'post', ['post_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'like', 'post', ['post_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'like', 'user', ['author'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'post', 'user', ['author'], ['id'], ondelete='CASCADE')
    op.add_column('user', sa.Column('userpublicname', sa.String(length=150), nullable=True))
    op.add_column('user', sa.Column('userlogo', sa.String(length=350), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'userlogo')
    op.drop_column('user', 'userpublicname')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'like', type_='foreignkey')
    op.drop_constraint(None, 'like', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    # ### end Alembic commands ###
