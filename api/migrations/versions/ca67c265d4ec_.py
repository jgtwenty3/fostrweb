"""empty message

Revision ID: ca67c265d4ec
Revises: 67dab6d5e400
Create Date: 2025-03-06 09:58:44.662913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca67c265d4ec'
down_revision = '67dab6d5e400'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('fk_users_owned_shelter_id_shelters', type_='foreignkey')
        batch_op.drop_column('owned_shelter_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('owned_shelter_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_users_owned_shelter_id_shelters', 'shelters', ['owned_shelter_id'], ['id'])

    # ### end Alembic commands ###
