from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import groups
from typing import List, Sequence


async def get_all_groups(session: AsyncSession) -> Sequence[groups]:
    result = await session.execute(select(groups))
    return result.scalars().all()


async def get_existing_group_names(session: AsyncSession) -> List[str]:
    groups_list = await get_all_groups(session)
    return [group.name for group in groups_list]


async def add_single_group(session: AsyncSession, group_name: str) -> groups:
    new_group = groups(name=group_name)
    session.add(new_group)
    await session.commit()
    await session.refresh(new_group)
    return new_group

