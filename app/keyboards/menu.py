from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Моё расписание"), KeyboardButton(text="Расписание других групп")],
    ],
    resize_keyboard=True
)
