from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import college_repository
from typing import List


async def get_colleges_array(session: AsyncSession) -> List[str]:
    existing_college = await college_repository.get_all(session)
    college_names = [college.name for college in existing_college]

    return college_names
