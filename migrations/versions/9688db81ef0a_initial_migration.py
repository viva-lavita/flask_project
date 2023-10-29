"""Initial migration.

Revision ID: 9688db81ef0a
Revises: 
Create Date: 2023-10-29 05:20:11.241580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9688db81ef0a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('intro', sa.String(length=300), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('author', sa.String(length=20), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=128), nullable=True),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('note')
    # ### end Alembic commands ###
