from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import AASKUsers, Groups
from app.crud.groups import get_group_by_name


async def create_user(
    session: AsyncSession, chat_id: str, group_name: str, username: str
):
    group = await get_group_by_name(session, group_name)
    if not group:
        raise ValueError(f"Группа {group_name} не найдена")

    # Проверяем существующего пользователя
    existing_user = await session.execute(
        select(AASKUsers).where(AASKUsers.chat_id == chat_id)
    )
    existing_user = existing_user.scalar_one_or_none()

    if existing_user:
        # Обновляем данные существующего пользователя
        existing_user.group_sid = group.sid
        existing_user.username = username
        await session.commit()
        return existing_user
    else:
        # Создаем нового пользователя
        user = AASKUsers(chat_id=str(chat_id), group_sid=group.sid, username=username)
        session.add(user)
        await session.commit()
        return user


async def get_all_group_ids(session: AsyncSession):
    stmt = select(AASKUsers.chat_id, Groups.name.label("group_name")).join(
        Groups, AASKUsers.group_sid == Groups.sid
    )

    result = await session.execute(stmt)
    return [
        {"chat_id": row.chat_id, "group_name": row.group_name} for row in result.all()
    ]
