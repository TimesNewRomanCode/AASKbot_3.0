from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.db.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import Address


class College(CoreModel):
    __tablename__ = "college"

    name: Mapped[str] = mapped_column(String, index=True)

    addresses: Mapped[list["Address"]] = relationship(
        "Address", back_populates="college"
    )
