import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.common.db.base_repository import BaseRepository
from app.models import Group, Address

from app.schemas.group import GroupUpdate, GroupCreate


class GroupRepository(BaseRepository[Group, GroupCreate, GroupUpdate]):
    @staticmethod
    async def get_group_by_name(session: AsyncSession, group_name: str):
        query = select(Group).where(Group.name == group_name)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_group_by_address(session: AsyncSession, address_name: str):
        query = (
            select(Group)
            .join(Address, Address.sid == Group.address_sid)
            .where(Address.name == address_name)
            .order_by(Group.name.asc())
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_group_by_address_sid(session: AsyncSession, address_sid: uuid.UUID):
        query = (
            select(Group)
            .join(Address, Address.sid == Group.address_sid)
            .where(Address.sid == address_sid)
            .order_by(Group.name.asc())
        )
        result = await session.execute(query)
        return result.scalars().all()


group_repository = GroupRepository(Group)
