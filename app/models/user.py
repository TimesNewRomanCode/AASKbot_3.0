from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UUID, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.db.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import Group


class User(CoreModel):
    __tablename__ = "user"

    chat_id: Mapped[str] = mapped_column(
        String, unique=True, primary_key=True, index=True
    )
    group_sid: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("group.sid", ondelete="CASCADE"), nullable=False
    )
    username: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    is_newsletter: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    group: Mapped["Group"] = relationship("Group", back_populates="users")
    group_name = association_proxy("group", "name")
