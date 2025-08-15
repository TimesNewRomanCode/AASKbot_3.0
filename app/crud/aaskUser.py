from sqlalchemy.ext.asyncio import AsyncSession
from app.models.aaskUsers import aaskUsers
from datetime import datetime

async def create_user(session: AsyncSession, chat_id: int, group_name: str, username: str, date_registr: datetime):
    user = aaskUsers(
        chat_id=chat_id,
        group_name=group_name,
        username=username,
        date_registr=date_registr
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
