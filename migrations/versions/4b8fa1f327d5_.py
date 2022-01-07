"""empty message

Revision ID: 4b8fa1f327d5
Revises: 
Create Date: 2021-12-21 10:21:46.458774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b8fa1f327d5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('board_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('owner', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('board_id')
    )
    op.create_table('card',
    sa.Column('card_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('likes_count', sa.String(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.board_id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('card_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('card')
    op.drop_table('board')
    # ### end Alembic commands ###
