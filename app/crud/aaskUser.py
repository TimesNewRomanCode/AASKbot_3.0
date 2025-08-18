from sqlalchemy.ext.asyncio import AsyncSession
from app.models.aaskUsers import aaskUsers
from datetime import datetime
from sqlalchemy import select
from app.services.pars import load_groups_from_file

GROUP_NAMES = load_groups_from_file()

async def create_user(session: AsyncSession,chat_id: int, group_name: str, username: str, date_registr: datetime):
    result = await session.execute(
        select(aaskUsers).where(aaskUsers.chat_id == chat_id)
    )
    user = result.scalars().first()

    if user:
        user.group_name = group_name
        user.username = username
        user.date_registr = date_registr
    else:
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

async def get_all_group_ids(session: AsyncSession):
    query = (
        select(aaskUsers.chat_id, aaskUsers.group_name)
        .where(aaskUsers.group_name.in_(GROUP_NAMES))
    )
    result = await session.execute(query)
    return result.mappings().all()