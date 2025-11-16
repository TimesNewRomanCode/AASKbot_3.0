from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column


from app.common.db.core_model import CoreModel


class Groups(CoreModel):
    __tablename__ = "groups"

    name: Mapped[str] = mapped_column(String, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
