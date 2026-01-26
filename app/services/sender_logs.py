from datetime import date

from app.models import SenderLogs
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import sender_logs_repository


async def quick_create_log(session: AsyncSession):
    new_log = SenderLogs()
    session.add(new_log)
    await session.commit()
    await session.refresh(new_log)
    return new_log

async def get_has_today_log(session: AsyncSession):
    last_date = await sender_logs_repository.get_sender_logs(session)

    return last_date != date.today()