"""empty message

Revision ID: 88f6aec7dd17
Revises: ca67c265d4ec
Create Date: 2025-03-06 10:02:27.738758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88f6aec7dd17'
down_revision = 'ca67c265d4ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('animals', schema=None) as batch_op:
        batch_op.drop_constraint('fk_animals_transport_id_users', type_='foreignkey')
        batch_op.drop_constraint('fk_animals_foster_id_users', type_='foreignkey')
        batch_op.drop_column('transport_id')
        batch_op.drop_column('foster_id')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('fk_users_shelter_id_shelters', type_='foreignkey')
        batch_op.drop_column('shelter_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shelter_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_users_shelter_id_shelters', 'shelters', ['shelter_id'], ['id'])

    with op.batch_alter_table('animals', schema=None) as batch_op:
        batch_op.add_column(sa.Column('foster_id', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('transport_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_animals_foster_id_users', 'users', ['foster_id'], ['id'])
        batch_op.create_foreign_key('fk_animals_transport_id_users', 'users', ['transport_id'], ['id'])

    # ### end Alembic commands ###
