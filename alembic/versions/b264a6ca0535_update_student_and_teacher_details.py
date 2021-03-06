"""Update student and teacher details

Revision ID: b264a6ca0535
Revises: 0fdc5ee5f004
Create Date: 2022-04-24 12:47:50.781348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b264a6ca0535'
down_revision = '0fdc5ee5f004'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('faculty_no', sa.String(length=30), nullable=True))
    op.add_column('students', sa.Column('enroll_no', sa.String(length=30), nullable=True))
    op.add_column('students', sa.Column('department_name', sa.String(length=30), nullable=True))
    op.create_unique_constraint(None, 'students', ['enroll_no'])
    op.create_unique_constraint(None, 'students', ['faculty_no'])
    op.add_column('teachers', sa.Column('department_name', sa.String(length=30), nullable=True))
    op.create_unique_constraint(None, 'teachers', ['department_name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'teachers', type_='unique')
    op.drop_column('teachers', 'department_name')
    op.drop_constraint(None, 'students', type_='unique')
    op.drop_constraint(None, 'students', type_='unique')
    op.drop_column('students', 'department_name')
    op.drop_column('students', 'enroll_no')
    op.drop_column('students', 'faculty_no')
    # ### end Alembic commands ###
