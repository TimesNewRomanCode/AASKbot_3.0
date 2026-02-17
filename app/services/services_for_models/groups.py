from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import group_repository
from typing import List

from app.schemas.group import GroupCreate


async def get_groups_array(session: AsyncSession, address_name) -> List[str]:
    existing_groups = await group_repository.get_group_by_address(session, address_name)
    group_names = [group.name for group in existing_groups]

    return group_names


async def get_groups_array_by_sid(session: AsyncSession, address_sid) -> List[str]:
    existing_groups = await group_repository.get_group_by_address_sid(
        session, address_sid
    )
    group_names = [group.name for group in existing_groups]

    return group_names


async def update_groups(session: AsyncSession, address_sid: UUID, groups: List[str]):
    group_names = await get_groups_array_by_sid(session, address_sid)
    missing_groups = [
        group_name for group_name in groups if group_name not in group_names
    ]
    for group_name in missing_groups:
        await group_repository.create(
            session,
            obj_in=GroupCreate(name=group_name, address_sid=address_sid),
            with_commit=False,
        )
        print(f"Добавлена группа: {group_name}")

    await session.commit()
