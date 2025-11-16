from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.aaskUser import create_user
from app.crud.groups import get_group_by_name


async def register_user(
    session: AsyncSession, chat_id: int, group_name: str, username: str
):
    group = await get_group_by_name(session, group_name)
    if not group:
        raise ValueError(f"Группа {group_name} не найдена в базе данных")

    return await create_user(session, str(chat_id), group_name, username)
