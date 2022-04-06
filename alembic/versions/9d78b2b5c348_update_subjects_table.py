"""Update subjects table

Revision ID: 9d78b2b5c348
Revises: e98e5336a7d9
Create Date: 2022-04-06 17:10:58.511383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d78b2b5c348'
down_revision = 'e98e5336a7d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subjects', sa.Column('code', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subjects', 'code')
    # ### end Alembic commands ###