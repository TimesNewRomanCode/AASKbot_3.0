from sqlalchemy import String, Integer, ForeignKey, UUID, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class aaskUsers(Base):
    __tablename__ = "aaskUsers"

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    group_sid: Mapped[UUID] = mapped_column(UUID, ForeignKey("groups.sid", ondelete="CASCADE"), nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)