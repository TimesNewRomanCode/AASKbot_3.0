from aiofiles import os
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile, InputMediaPhoto

from app.core.database import AsyncSessionLocal
from app.keyboards.schedule_manager_keyboards import get_gallery_keyboard
from app.services.get_photo_for_manager import send_current_photo,  get_photo_paths_from_db

schedule_manager = Router()

user_photo_index = {}


@schedule_manager.message(Command("gallery"))
async def start_gallery(message: types.Message):
    chat_id = message.from_user.id
    user_photo_index[chat_id] = 0

    photo_paths = await get_photo_paths_from_db(chat_id)
    print(photo_paths)
    await send_current_photo(message.chat.id, chat_id, user_photo_index, photo_paths)

@schedule_manager.callback_query(lambda c: c.data in ['prev', 'next', 'close'])
async def handle_gallery_controls(callback: types.CallbackQuery):
    chat_id = callback.from_user.id

    if callback.data == "close":
        await callback.message.delete()
        await callback.answer("Галерея закрыта")
        return


    photo_paths = await get_photo_paths_from_db(chat_id)

    if not photo_paths:
        await callback.answer("❌ Нет доступных фото")
        return

    current_index = user_photo_index.get(chat_id, 0)

    if callback.data == "prev":
        new_index = (current_index - 1) % len(photo_paths)
    elif callback.data == "next":
        new_index = (current_index + 1) % len(photo_paths)
    else:
        new_index = current_index

    user_photo_index[chat_id] = new_index
    photo_path = photo_paths[new_index % len(photo_paths)]

    if os.path.exists(photo_path):
        new_media = InputMediaPhoto(
            media=FSInputFile(photo_path),
            caption=f"Фото {new_index + 1} из {len(photo_paths)}"
        )

        keyboard = get_gallery_keyboard(new_index, len(photo_paths))

        await callback.message.edit_media(
            media=new_media,
            reply_markup=keyboard
        )

    await callback.answer()