"""create posts table

Revision ID: 3a943b31bee8
Revises: 
Create Date: 2023-07-18 17:11:58.715225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a943b31bee8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column(
        'id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
