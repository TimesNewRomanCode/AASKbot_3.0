from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Узнать расписание")],
    ],
    resize_keyboard=True
)
