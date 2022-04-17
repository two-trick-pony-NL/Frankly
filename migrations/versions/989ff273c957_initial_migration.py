"""Initial migration.

Revision ID: 989ff273c957
Revises: 
Create Date: 2022-04-10 19:33:18.576306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '989ff273c957'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'campaign', 'user', ['author'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comment', 'user', ['author'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'comment', 'post', ['post_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'like', 'user', ['author'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'like', 'post', ['post_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'post', 'user', ['author'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'post', 'campaign', ['campaign'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'like', type_='foreignkey')
    op.drop_constraint(None, 'like', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'campaign', type_='foreignkey')
    # ### end Alembic commands ###