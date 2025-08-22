from sqlalchemy import ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column


from .base import Base


class groups(Base):
    __tablename__ = "groups"

    groups: Mapped[list[str]] = mapped_column(ARRAY(String), primary_key=True, nullable=False)