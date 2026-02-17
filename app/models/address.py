from typing import TYPE_CHECKING

from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.db.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import Group, College


class Address(CoreModel):
    __tablename__ = "address"

    name: Mapped[str] = mapped_column(String, index=True)
    college_sid: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("college.sid", ondelete="CASCADE"), nullable=True
    )

    groups: Mapped[list["Group"]] = relationship("Group", back_populates="address")

    college: Mapped["College"] = relationship("College", back_populates="addresses")
    college_name = association_proxy("college", "name")
