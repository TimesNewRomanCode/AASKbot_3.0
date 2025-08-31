from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class aaskUsers(Base):
    __tablename__ = "aaskUsers"

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    group_sid: Mapped[str] = mapped_column(ForeignKey("groups.sid", ondelete="CASCADE"), String,nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)