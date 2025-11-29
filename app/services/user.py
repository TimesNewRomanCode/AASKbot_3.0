from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import group_repository, user_repository
from app.schemas.user import UserCreate


async def register_user(
    session: AsyncSession,
    chat_id: int,
    group_name: str,
    username: str
):
    chat_id = str(chat_id)
    group = await group_repository.get_group_by_name(session, group_name)
    if not group:
        raise ValueError(f"Группа {group_name} не найдена в базе данных")

    user = await user_repository.get_by_chat_id(session, chat_id)
    if user:
        user.group_sid = group.sid
        user.username = username
        user.is_active = True
        await session.commit()
    else:
        user = await user_repository.create(
            session,
            obj_in=UserCreate(
                username=username, chat_id=chat_id, is_active=True, group_sid=group.sid
            ),
        )

    return user
