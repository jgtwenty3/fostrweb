"""empty message

Revision ID: 461a64b194a6
Revises: 88f6aec7dd17
Create Date: 2025-03-06 10:15:23.882192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '461a64b194a6'
down_revision = '88f6aec7dd17'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shelters', schema=None) as batch_op:
        batch_op.alter_column('owner_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shelter_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_users_shelter_id_shelters'), 'shelters', ['shelter_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_users_shelter_id_shelters'), type_='foreignkey')
        batch_op.drop_column('shelter_id')

    with op.batch_alter_table('shelters', schema=None) as batch_op:
        batch_op.alter_column('owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
