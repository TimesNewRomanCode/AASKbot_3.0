from aiofiles import os
from aiogram.types import FSInputFile
from app.core.create_bot import bot
from app.core.database import AsyncSessionLocal
from app.keyboards.schedule_manager_keyboards import get_gallery_keyboard
from datetime import datetime, timedelta
from app.repositories.user_repository import user_repository


async def send_current_photo(chat_id, photo_paths):
    today = datetime.now()
    day_month = int(today.strftime("%d%m"))
    tomorrow = (datetime.now() - timedelta(days=0)).strftime("%d.%m.%Y")

    if not photo_paths:
        await bot.send_message(chat_id, "Пока рассписания нет")
        return

    photo_path = f"{photo_paths[0]}{day_month}{photo_paths[1]}"
    print(photo_path)
    keyboard = get_gallery_keyboard()

    try:
        await bot.send_photo(
            chat_id=chat_id,
            photo=FSInputFile(photo_path),
            caption=tomorrow,
            reply_markup=keyboard
        )
    except Exception as e:
        await bot.send_message(
            chat_id=chat_id,
            text=f"На дату {tomorrow} рассписание не найденно",
            reply_markup=keyboard
        )


async def get_photo_paths_from_db(chat_id: int) -> list:
    try:
        async with AsyncSessionLocal() as session:
            user = await user_repository.get_by_chat_id(session, str(chat_id))
            folder_path = "app/grop_photo/ААСК/"
            group_path = f"/{user.group_name}.png"
            return [folder_path, group_path]

    except Exception as e:
        print(f"Ошибка при получении путей фото: {e}")
        return []