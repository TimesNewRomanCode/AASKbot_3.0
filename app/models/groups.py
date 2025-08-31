from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base


class groups(Base):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, index=True)