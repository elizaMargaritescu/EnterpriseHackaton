"""second migration

Revision ID: 9b7e91762738
Revises: 
Create Date: 2021-04-17 01:25:13.021370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b7e91762738'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=200), nullable=True))
        batch_op.add_column(sa.Column('likes', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('postingTime', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_posts_description'), ['description'], unique=False)
        batch_op.create_index(batch_op.f('ix_posts_likes'), ['likes'], unique=False)
        batch_op.create_index(batch_op.f('ix_posts_postingTime'), ['postingTime'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_posts_postingTime'))
        batch_op.drop_index(batch_op.f('ix_posts_likes'))
        batch_op.drop_index(batch_op.f('ix_posts_description'))
        batch_op.drop_column('postingTime')
        batch_op.drop_column('likes')
        batch_op.drop_column('description')

    # ### end Alembic commands ###