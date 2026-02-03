"""Изменение модели user(is_newsletter)

Revision ID: f965d5d85d2e
Revises: c605822246cf
Create Date: 2026-02-03 16:39:18.737300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f965d5d85d2e'
down_revision: Union[str, None] = 'c605822246cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'user',
        sa.Column('is_newsletter', sa.Boolean(), nullable=False, server_default=sa.true())
    )
    op.create_index('ix_user_is_newsletter', 'user', ['is_newsletter'])

def downgrade() -> None:
    op.drop_index('ix_user_is_newsletter', table_name='user')
    op.drop_column('user', 'is_newsletter')