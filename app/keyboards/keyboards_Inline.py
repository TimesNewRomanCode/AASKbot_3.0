from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.services.groups import select_groups
from sqlalchemy.ext.asyncio import AsyncSession


async def get_inline_kb(session: AsyncSession) -> InlineKeyboardMarkup:
    groups = await select_groups(session)
    if not groups:
        groups = ["Нет групп"]

    buttons = [InlineKeyboardButton(text=group, callback_data=f"btn_{group}") for group in groups]
    keyboard_layout = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
