from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import address_repository
from typing import List


async def get_addresses_array(session: AsyncSession, college_name) -> List[str]:
    existing_address = await address_repository.get_address_by_college(
        session, college_name
    )
    address_names = [address.name for address in existing_address]

    return address_names
