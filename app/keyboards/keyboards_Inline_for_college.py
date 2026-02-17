from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.services_for_models.college import get_colleges_array
from sqlalchemy.ext.asyncio import AsyncSession


async def get_inline_kb_for_college(session: AsyncSession) -> InlineKeyboardMarkup:
    colleges = await get_colleges_array(session)
    if not colleges:
        colleges = ["Нет колледжей"]

    buttons = [
        InlineKeyboardButton(text=college, callback_data=f"college_{college}")
        for college in colleges
    ]
    keyboard_layout = [buttons[i : i + 4] for i in range(0, len(buttons), 4)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
