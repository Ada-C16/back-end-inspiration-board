"""empty message

Revision ID: 24d394439af0
Revises: f7247d47d9cb
Create Date: 2021-12-30 14:33:34.901030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24d394439af0'
down_revision = 'f7247d47d9cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('board', 'owner',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('board', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('card', sa.Column('board_id', sa.Integer(), nullable=False))
    op.alter_column('card', 'message',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_foreign_key(None, 'card', 'board', ['board_id'], ['board_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'card', type_='foreignkey')
    op.alter_column('card', 'message',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('card', 'board_id')
    op.alter_column('board', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('board', 'owner',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
