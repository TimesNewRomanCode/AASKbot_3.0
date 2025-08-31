from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.models.aaskUsers import aaskUsers
from datetime import datetime
from sqlalchemy import select
from app.services.groups import get_groups_array



async def create_user(session: AsyncSession,chat_id: int, group_name: str, username: str):
    result = await session.execute(
        select(aaskUsers).where(aaskUsers.chat_id == chat_id)
    )
    user = result.scalars().first()

    if user:
        user.group_name = group_name
        user.username = username
    else:
        user = aaskUsers(
            chat_id=chat_id,
            group_name=group_name,
            username=username
        )
        session.add(user)

    await session.commit()
    await session.refresh(user)
    return user

async def get_all_group_ids(session: AsyncSession):
    group = await get_groups_array(session)
    query = (
        select(aaskUsers.chat_id, aaskUsers.group_name)
        .where(aaskUsers.group_name.in_(group))
    )
    result = await session.execute(query)
    return result.mappings().all()