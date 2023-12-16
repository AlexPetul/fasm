"""add prepositions attr

Revision ID: f4d635757355
Revises: 4af7e330fef8
Create Date: 2023-12-10 16:24:38.162613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4d635757355'
down_revision = '4af7e330fef8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vocabulary', schema=None) as batch_op:
        batch_op.add_column(sa.Column('preposition', sa.Boolean(), server_default=sa.text('false'), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('vocabulary', schema=None) as batch_op:
        batch_op.drop_column('preposition')

    # ### end Alembic commands ###