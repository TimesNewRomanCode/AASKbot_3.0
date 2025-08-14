from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .base import Base


class aaskUsers(Base):
    __tablename__ = "aaskUsers"

    chat_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    group_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    date_registr: Mapped[datetime] = mapped_column(DateTime, unique=False, nullable=False)
