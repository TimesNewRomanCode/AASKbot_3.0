from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Groups
from typing import List, Sequence


async def get_all_groups(session: AsyncSession) -> Sequence[Groups]:
    result = await session.execute(select(Groups))
    return result.scalars().all()


async def get_existing_group_names(session: AsyncSession) -> List[str]:
    groups_list = await get_all_groups(session)
    return [group.name for group in groups_list]


async def add_single_group(session: AsyncSession, group_name: str) -> Groups:
    new_group = Groups(name=group_name)
    session.add(new_group)
    await session.commit()
    await session.refresh(new_group)
    return new_group


async def get_group_by_name(session: AsyncSession, group_name: str):
    result = await session.execute(select(Groups).where(Groups.name == group_name))
    return result.scalar_one_or_none()


async def get_group_by_sid(session: AsyncSession, group_sid: str):
    result = await session.execute(select(Groups).where(Groups.sid == group_sid))
    return result.scalar_one_or_none()
