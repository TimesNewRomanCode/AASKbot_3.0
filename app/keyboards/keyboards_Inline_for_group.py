from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.services.services_for_models.groups import get_groups_array
from sqlalchemy.ext.asyncio import AsyncSession


async def get_inline_kb_for_group(
    session: AsyncSession, address_name: str
) -> InlineKeyboardMarkup:
    groups = await get_groups_array(session, address_name)
    if not groups:
        groups = ["Нет групп"]

    buttons = [
        InlineKeyboardButton(text=group, callback_data=f"btn_{group}")
        for group in groups
    ]
    keyboard_layout = [buttons[i : i + 4] for i in range(0, len(buttons), 4)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
