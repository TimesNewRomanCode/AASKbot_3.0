from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.common.db.base_repository import BaseRepository
from app.models import Address, College
from app.schemas.address import AddressCreate, AddressUpdate


class AddressRepository(BaseRepository[Address, AddressCreate, AddressUpdate]):
    @staticmethod
    async def get_address_by_name(session: AsyncSession, address_name: str):
        stmt = select(Address).where(Address.name == address_name)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_address_by_college(session: AsyncSession, college_name: str):
        stmt = (
            select(Address)
            .join(College, College.sid == Address.college_sid)
            .where(College.name == college_name)
            .order_by(Address.name.asc())
        )
        result = await session.execute(stmt)
        return result.scalars().all()


address_repository = AddressRepository(Address)
