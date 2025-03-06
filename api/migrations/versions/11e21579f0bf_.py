"""empty message

Revision ID: 11e21579f0bf
Revises: b3c5edc1010b
Create Date: 2025-03-06 16:43:33.681957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11e21579f0bf'
down_revision = 'b3c5edc1010b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_constraint('fk_messages_animal_id_animals', type_='foreignkey')
        batch_op.drop_column('animal_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('animal_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_messages_animal_id_animals', 'animals', ['animal_id'], ['id'])

    # ### end Alembic commands ###
