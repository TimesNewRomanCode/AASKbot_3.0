from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import groups


async def overwrite_groups_array(session: AsyncSession, new_groups: list[str]) -> groups:

    result = await session.execute(select(groups))
    groups_record = result.scalars().first()
    groups_record.groups = new_groups

    await session.commit()
    await session.refresh(groups_record)
    return groups_record


async def get_current_groups(session: AsyncSession) -> list[str]:

    result = await session.execute(select(groups))
    groups_record = result.scalars().first()

    if groups_record:
        return groups_record.groups
    else:
        return []