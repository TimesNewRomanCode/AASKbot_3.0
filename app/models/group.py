from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, UUID, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.db.core_model import CoreModel

if TYPE_CHECKING:
    from app.models import User, Address


class Group(CoreModel):
    __tablename__ = "group"

    name: Mapped[str] = mapped_column(String, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)

    address_sid: Mapped[UUID] = mapped_column(
        UUID, ForeignKey("address.sid", ondelete="CASCADE"), nullable=True
    )

    users: Mapped[list["User"]] = relationship("User", back_populates="group")

    address: Mapped["Address"] = relationship("Address", back_populates="groups")
    address_name = association_proxy("address", "name")
    college_name = association_proxy("address", "college_name")
