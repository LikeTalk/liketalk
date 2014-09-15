"""empty message

Revision ID: 177ebe91a4b4
Revises: None
Create Date: 2014-09-07 15:05:23.772762

"""

# revision identifiers, used by Alembic.
revision = '177ebe91a4b4'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_history',
    sa.Column('GameHistory_id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(length=255), nullable=True),
    sa.Column('done_game', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('GameHistory_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game_history')
    ### end Alembic commands ###