"""change table names

Revision ID: 402e64d0126e
Revises: 9f99a533daf4
Create Date: 2025-11-22 16:39:32.778977
"""

from typing import Union, Sequence
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "402e64d0126e"
down_revision: Union[str, None] = "9f99a533daf4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("groups", "group")
    op.rename_table("aaskUsers", "user")


def downgrade() -> None:
    op.rename_table("group", "groups")
    op.rename_table("user", "aaskUsers")
