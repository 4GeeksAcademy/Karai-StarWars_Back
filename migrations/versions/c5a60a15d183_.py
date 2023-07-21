"""empty message

Revision ID: c5a60a15d183
Revises: 9b153de5a208
Create Date: 2023-07-20 19:37:27.201286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5a60a15d183'
down_revision = '9b153de5a208'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_column('homeworld')

    with op.batch_alter_table('starship', schema=None) as batch_op:
        batch_op.add_column(sa.Column('max_atmosphering_speed', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('passangers', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('starship_class', sa.String(length=250), nullable=True))
        batch_op.drop_column('max_atmosphering_speed')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('starship', schema=None) as batch_op:
        batch_op.add_column(sa.Column('max_atmosphering_speed', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
        batch_op.drop_column('starship_class')
        batch_op.drop_column('passangers')
        batch_op.drop_column('max_atmosphering_speed')

    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('homeworld', sa.VARCHAR(length=250), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
