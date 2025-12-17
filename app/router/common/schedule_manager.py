from datetime import datetime, timedelta
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from app.keyboards.schedule_manager_keyboards import get_gallery_keyboard
from app.services.get_photo_for_manager import send_current_photo,  get_photo_paths_from_db

schedule_manager = Router()

class UserState(StatesGroup):
    current_date = State()

@schedule_manager.message(Command("schedule"))
async def start_gallery(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id

    await state.update_data(current_date=datetime.now())

    photo_paths = await get_photo_paths_from_db(chat_id)
    await send_current_photo(chat_id, photo_paths)


@schedule_manager.callback_query(lambda c: c.data in ['prev', 'next'])
async def handle_gallery_controls(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    photo_paths = await get_photo_paths_from_db(chat_id)

    data = await state.get_data()
    current_date = data.get('current_date', datetime.now())

    if not photo_paths:
        await callback.answer("Нет доступных фото")
        return

    if callback.data == "prev":
        current_date = current_date - timedelta(days=1)
    elif callback.data == "next":
        current_date = current_date + timedelta(days=1)

    elif callback.data == "today":
        current_date = datetime.now()

    await state.update_data(current_date=current_date)

    tomorrow = current_date.strftime("%d.%m.%Y")
    day_month = int(current_date.strftime("%d%m"))

    photo_path = f"{photo_paths[0]}{day_month}{photo_paths[1]}"

    new_media = InputMediaPhoto(
        media=FSInputFile(photo_path),
        caption=f"{tomorrow}"
    )

    placeholder_media = InputMediaPhoto(
        media="https://i.pinimg.com/736x/b8/37/f0/b837f05af4779d60029b2aa327bd9050.jpg",
        caption=f"На дату {tomorrow} рассписания не найдено"
    )

    keyboard = get_gallery_keyboard()

    try:
        await callback.message.edit_media(
            media=new_media,
            reply_markup=keyboard
        )
    except Exception as e:
        await callback.message.edit_media(
            media=placeholder_media,
            reply_markup=keyboard
        )

    await callback.answer()