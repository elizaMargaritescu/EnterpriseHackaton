"""third migration

Revision ID: 41dc7c52a8b7
Revises: 9b7e91762738
Create Date: 2021-04-17 10:52:57.137511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41dc7c52a8b7'
down_revision = '9b7e91762738'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.drop_index('ix_customer_phone')
        batch_op.drop_column('phone')

    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tags', sa.String(length=200), nullable=True))
        batch_op.create_index(batch_op.f('ix_posts_tags'), ['tags'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_posts_tags'))
        batch_op.drop_column('tags')

    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone', sa.VARCHAR(length=11), nullable=True))
        batch_op.create_index('ix_customer_phone', ['phone'], unique=False)

    # ### end Alembic commands ###
