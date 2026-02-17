"""Add address relation to group

Revision ID: 59464171fe0a
Revises: 520c638b669e
Create Date: 2026-02-05 22:01:04.377677
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "59464171fe0a"
down_revision: Union[str, None] = "520c638b669e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "group",
        sa.Column("address_sid", sa.UUID(), nullable=True),
    )

    op.create_foreign_key(
        "fk_group_address_sid",
        source_table="group",
        referent_table="address",
        local_cols=["address_sid"],
        remote_cols=["sid"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_group_address_sid",
        "group",
        type_="foreignkey",
    )

    op.drop_column("group", "address_sid")
