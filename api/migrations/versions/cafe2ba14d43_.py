"""empty message

Revision ID: cafe2ba14d43
Revises: 9b2c73904a7f
Create Date: 2025-03-06 20:14:39.480739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cafe2ba14d43'
down_revision = '9b2c73904a7f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('animal_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_posts_animal_id_animals'), 'animals', ['animal_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_posts_animal_id_animals'), type_='foreignkey')
        batch_op.drop_column('animal_id')

    # ### end Alembic commands ###
