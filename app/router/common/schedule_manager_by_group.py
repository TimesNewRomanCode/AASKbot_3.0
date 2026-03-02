from datetime import datetime, timedelta
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, InputMediaPhoto, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.kb_for_manager import kb_for_manager
from app.keyboards.schedule_manager_keyboards import get_gallery_keyboard_by_group
from app.repositories import user_repository
from app.services.get_photo_for_manager import (
    get_photo_paths_from_db_by_group, send_current_photo_by_group,
)

schedule_manager_by_group = Router()


class UserState(StatesGroup):
    current_date = State()
    group_name = State()

@schedule_manager_by_group.message(F.text == "Расписание других групп")
async def start_gallery(message: types.Message, session: AsyncSession):
    chat_id = str(message.chat.id)
    user = await user_repository.get_by_chat_id(session, chat_id)
    address_name = user.address_name
    kb = await kb_for_manager(session, address_name)
    await message.answer("Выберете группу расписание которой вы хотите увидеть", reply_markup=kb)

@schedule_manager_by_group.callback_query(F.data.startswith("group_"))
async def process_order_callback_for_group(
    callback_query: CallbackQuery, state: FSMContext
):
    print(callback_query.data.split("_")[1])
    group_name = callback_query.data.split("_")[1]
    await state.update_data(group_name=group_name)
    chat_id = callback_query.from_user.id
    await state.update_data(current_date=datetime.now())
    await callback_query.answer()
    photo_paths = await get_photo_paths_from_db_by_group(chat_id, group_name)
    chat_id = callback_query.from_user.id
    await send_current_photo_by_group(chat_id, photo_paths)
    await callback_query.message.delete()



@schedule_manager_by_group.callback_query(lambda c: c.data in ["prev1", "next1"])
async def handle_gallery_controls(callback: types.CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    print(chat_id)
    data = await state.get_data()
    group_name = data.get("group_name")
    photo_paths = await get_photo_paths_from_db_by_group(chat_id, group_name)

    current_date = data.get("current_date", datetime.now())

    if not photo_paths:
        await callback.answer("Нет доступных фото")
        return

    if callback.data == "prev1":
        current_date = current_date - timedelta(days=1)
    elif callback.data == "next1":
        current_date = current_date + timedelta(days=1)

    elif callback.data == "today":
        current_date = datetime.now()

    await state.update_data(current_date=current_date)

    tomorrow = current_date.strftime("%d.%m.%Y")
    day_month = int(current_date.strftime("%d%m"))
    photo_path = f"{photo_paths[0]}{day_month}{photo_paths[1]}"

    new_media = InputMediaPhoto(media=FSInputFile(photo_path), caption=f"{tomorrow}")

    placeholder_media = InputMediaPhoto(
        media="https://i.pinimg.com/736x/b8/37/f0/b837f05af4779d60029b2aa327bd9050.jpg",
        caption=f"На дату {tomorrow} расписания не найдено",
    )

    keyboard = get_gallery_keyboard_by_group()

    try:
        await callback.message.edit_media(media=new_media, reply_markup=keyboard)
    except Exception:
        await callback.message.edit_media(
            media=placeholder_media, reply_markup=keyboard
        )

    await callback.answer()
