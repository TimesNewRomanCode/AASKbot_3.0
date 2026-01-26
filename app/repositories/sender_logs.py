from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.common.db.base_repository import BaseRepository
from app.models import SenderLogs

from app.schemas.sender_logs import SenderLogsCreate, SenderLogsUpdate


class SenderLogsRepository(BaseRepository[SenderLogs, SenderLogsCreate, SenderLogsUpdate]):
    @staticmethod
    async def get_sender_logs(session: AsyncSession):
        stmt = select(func.max(SenderLogs.created_at))
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


sender_logs_repository = SenderLogsRepository(SenderLogs)
