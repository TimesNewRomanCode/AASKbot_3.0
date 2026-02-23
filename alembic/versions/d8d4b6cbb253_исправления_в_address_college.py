"""Исправления в address, college

Revision ID: d8d4b6cbb253
Revises: 59464171fe0a
Create Date: 2026-02-23 19:43:37.483110
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d8d4b6cbb253"
down_revision: Union[str, None] = "59464171fe0a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем колонку college_sid в address
    op.add_column(
        "address",
        sa.Column("college_sid", sa.UUID(), nullable=True),
    )

    # Создаем внешний ключ
    op.create_foreign_key(
        "fk_address_college_sid",
        source_table="address",
        referent_table="college",
        local_cols=["college_sid"],
        remote_cols=["sid"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # Удаляем внешний ключ
    op.drop_constraint(
        "fk_address_college_sid",
        "address",
        type_="foreignkey",
    )

    # Удаляем колонку
    op.drop_column("address", "college_sid")