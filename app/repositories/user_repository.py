from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.common.db.base_repository import BaseRepository
from app.models import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_chat_id(self, session: AsyncSession, chat_id: int):
        stmt = select(User).where(User.chat_id == chat_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


user_repository = UserRepository(User)
