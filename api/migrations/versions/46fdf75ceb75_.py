"""empty message

Revision ID: 46fdf75ceb75
Revises: 8a6562be4e1b
Create Date: 2025-03-05 16:34:09.352506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46fdf75ceb75'
down_revision = '8a6562be4e1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shelters', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.alter_column('owner_id',
               existing_type=sa.NUMERIC(),
               type_=sa.Integer(),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shelter_id', sa.Integer(), nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.NUMERIC(),
               type_=sa.Integer(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.create_foreign_key(batch_op.f('fk_users_shelter_id_shelters'), 'shelters', ['shelter_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_users_shelter_id_shelters'), type_='foreignkey')
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(),
               existing_nullable=False,
               autoincrement=True)
        batch_op.drop_column('shelter_id')

    with op.batch_alter_table('shelters', schema=None) as batch_op:
        batch_op.alter_column('owner_id',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('id',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(),
               existing_nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###
