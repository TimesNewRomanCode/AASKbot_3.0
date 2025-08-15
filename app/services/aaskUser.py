from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.aaskUser import create_user

async def register_user(session: AsyncSession, chat_id: int, group_name: str, username: str):
    date_registr = datetime.now()
    return await create_user(session, chat_id, group_name, username, date_registr)
