from datetime import datetime

from sqlalchemy import func, Date, cast
from sqlalchemy.orm import Mapped, mapped_column

from app.common.db.core_model import CoreModel

class SenderLogs(CoreModel):
    __tablename__ = "sender_logs"

    created_at: Mapped[datetime] = mapped_column(default=cast(func.now(), Date), nullable=False)


