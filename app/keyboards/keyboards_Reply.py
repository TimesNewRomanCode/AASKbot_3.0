from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def verification():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Узнать рассписание"),
                KeyboardButton(text="Изменить свою группу"),
                KeyboardButton(text="Добавить ещё одну группу"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Это точно ваша группа?",
    )
