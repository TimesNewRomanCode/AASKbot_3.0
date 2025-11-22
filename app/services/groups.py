from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import group_repository
from typing import List

from app.schemas.group import GroupCreate


async def get_groups_array(session: AsyncSession) -> List[str]:
    existing_groups = await group_repository.get_all(session)
    group_names = [group.name for group in existing_groups]

    return group_names


async def up_groups(session: AsyncSession, groups: List[str]):
    group_names = await get_groups_array(session)

    missing_groups = [
        group_name for group_name in groups if group_name not in group_names
    ]

    for group_name in missing_groups:
        await group_repository.create(
            session, obj_in=GroupCreate(name=group_name), with_commit=False
        )
        print(f"Добавлена группа: {group_name}")

    await session.commit()
