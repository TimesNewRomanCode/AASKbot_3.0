from aiofiles import os
from aiogram.types import FSInputFile
from app.core.create_bot import bot
from app.core.database import AsyncSessionLocal
from app.keyboards.schedule_manager_keyboards import get_gallery_keyboard
from datetime import datetime, timedelta
import os
from app.repositories.user_repository import user_repository


async def send_current_photo(chat_id, user_id, user_photo_index, photo_paths):
    current_index = user_photo_index.get(user_id, 0)

    if not photo_paths:
        await bot.send_message(chat_id, "Пока рассписания нет")
        return

    photo_path = photo_paths[current_index % len(photo_paths)]
    keyboard = get_gallery_keyboard(current_index, len(photo_paths))

    if os.path.exists(photo_path):
        await bot.send_photo(
            chat_id=chat_id,
            photo=FSInputFile(photo_path),
            caption=f"Фото {current_index + 1} из {len(photo_paths)}",
            reply_markup=keyboard
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text="Фото не найдено",
            reply_markup=keyboard
        )


async def get_photo_paths_from_db(chat_id: int) -> list:
    try:
        async with AsyncSessionLocal() as session:
            user = await user_repository.get_by_chat_id(session, str(chat_id))
            group = user.group
            today = datetime.now()
            target_day = today + timedelta(days=1)
            day_month = int(target_day.strftime("%d%m"))

            file_path = f"./app/grop_photo/ААСК/{day_month}/{group}.png"
            file_path = os.path.normpath(file_path)

            print(f"Сформирован путь для пользователя {chat_id}: {file_path}")
            return [file_path]

    except Exception as e:
        print(f"Ошибка при получении путей фото: {e}")
        return []