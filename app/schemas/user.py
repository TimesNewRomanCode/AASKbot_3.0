from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    chat_id: str
    group_sid: UUID | None
    username: str | None
    is_active: bool | None


class UserUpdate(BaseModel):
    group_sid: UUID | None
    username: str | None
    is_active: bool | None
