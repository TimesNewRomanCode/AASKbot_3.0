from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.groups import get_existing_group_names, add_single_group, get_all_groups
from typing import List


async def up_groups(session: AsyncSession, groups: List[str]):

    existing_groups = await get_existing_group_names(session)

    missing_groups = [
        group_name for group_name in groups
        if group_name not in existing_groups
    ]

    added_groups = []
    for group_name in missing_groups:

        new_group = await add_single_group(session, group_name)
        added_groups.append(new_group)
        print(f"Добавлена группа: {group_name}")

    return added_groups


async def get_groups_array(session: AsyncSession) -> List[str]:

    groups_objects = await get_all_groups(session)
    groups_array = [group.name for group in groups_objects]

    return groups_array