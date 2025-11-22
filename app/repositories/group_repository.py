from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.common.db.base_repository import BaseRepository
from app.models import Group

from app.schemas.group import GroupUpdate, GroupCreate


class GroupRepository(BaseRepository[Group, GroupCreate, GroupUpdate]):
    @staticmethod
    async def get_group_by_name(session: AsyncSession, group_name: str):
        stmt = select(Group).where(Group.name == group_name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


group_repository = GroupRepository(Group)
