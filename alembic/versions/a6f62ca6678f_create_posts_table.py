"""create posts table

Revision ID: a6f62ca6678f
Revises: 
Create Date: 2022-02-10 20:36:49.218441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6f62ca6678f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    

    pass


def downgrade():
    op.drop_table('posts')
    pass
