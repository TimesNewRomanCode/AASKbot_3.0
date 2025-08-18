from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from app.services.pars import load_groups_from_file

GROUP_NAMES = load_groups_from_file()

buttons = [InlineKeyboardButton(text=group, callback_data=f"btn_{group}") for group in GROUP_NAMES]

keyboard_layout = [buttons[i:i + 4] for i in range(0, len(buttons), 4)]
inline_kb1 = InlineKeyboardMarkup(inline_keyboard=keyboard_layout)
