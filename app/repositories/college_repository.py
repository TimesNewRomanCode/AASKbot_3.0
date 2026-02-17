from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.common.db.base_repository import BaseRepository
from app.models import College
from app.schemas.college import CollegeUpdate, CollegeCreate


class CollegeRepository(BaseRepository[College, CollegeCreate, CollegeUpdate]):
    @staticmethod
    async def get_college_by_name(session: AsyncSession, college_name: str):
        stmt = (
            select(College)
            .where(College.name == college_name)
            .order_by(College.name.asc())
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


college_repository = CollegeRepository(College)
