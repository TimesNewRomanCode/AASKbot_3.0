from aiogram import types

def get_gallery_keyboard(current_index: int, total_photos: int) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="⬅️", callback_data="prev"),
            types.InlineKeyboardButton(
                text=f"{current_index + 1}/{total_photos}",
                callback_data="counter"
            ),
            types.InlineKeyboardButton(text="➡️", callback_data="next")
        ]
    ])