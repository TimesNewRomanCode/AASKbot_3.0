from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.services.services_for_models.address import get_addresses_array
from sqlalchemy.ext.asyncio import AsyncSession


async def get_inline_kb_for_address(
    session: AsyncSession, college_name: str
) -> InlineKeyboardMarkup:
    addresses = await get_addresses_array(session, college_name)
    if not addresses:
        addresses = ["Нет адресов"]
    buttons = [
        InlineKeyboardButton(text=address, callback_data=f"address_{address}")
        for address in addresses
    ]
    keyboard_layout = [buttons[i : i + 4] for i in range(0, len(buttons), 4)]
    return InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
