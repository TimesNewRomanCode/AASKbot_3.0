from aiogram import types

def get_gallery_keyboard() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="⬅️", callback_data="prev"),
            types.InlineKeyboardButton(text="➡️", callback_data="next")
        ]
    ])