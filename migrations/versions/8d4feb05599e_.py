"""empty message

Revision ID: 8d4feb05599e
Revises: 
Create Date: 2021-12-23 11:20:17.690474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d4feb05599e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pass
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.create_table('board',
#     sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
#     sa.Column('name', sa.String(length=250), nullable=False),
#     sa.PrimaryKeyConstraint('id')
#     )
#     op.create_table('card',
#     sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
#     sa.Column('board_id', sa.Integer(), nullable=False),
#     sa.Column('value', sa.String(), nullable=False),
#     sa.Column('num_likes', sa.Integer(), nullable=True),
#     sa.ForeignKeyConstraint(['board_id'], ['board.id'], ),
#     sa.PrimaryKeyConstraint('id')
#     )
#     # ### end Alembic commands ###


def downgrade():
    pass
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.drop_table('card')
#     op.drop_table('board')
#     # ### end Alembic commands ###
