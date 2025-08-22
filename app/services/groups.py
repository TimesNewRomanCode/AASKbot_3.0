from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.groups import overwrite_groups_array, get_current_groups

async def up_groups(session: AsyncSession, groups: list[str]):
    return await overwrite_groups_array(session,  groups)

async def select_groups(session: AsyncSession) -> list[str]:
    return await get_current_groups(session)