from aiogram import types

def newsletter_of() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Отписаться от рассылки", callback_data="newsletter_of")
        ]
    ])