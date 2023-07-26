"""add content column

Revision ID: c2c9d7c9629e
Revises: 3a943b31bee8
Create Date: 2023-07-18 17:22:18.522191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2c9d7c9629e'
down_revision = '3a943b31bee8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
