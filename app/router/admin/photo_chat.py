from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.core.database import AsyncSessionLocal
import os
from app.core.create_bot import bot
from app.crud.aaskUser import get_all_group_ids

photo_chat_all_router = Router()


class WaitForMessage(StatesGroup):
    waiting = State()

@photo_chat_all_router.message(Command("photoAll"))
async def message_chat(message: types.Message, state: FSMContext):

    YOUR_CHAT_ID = 1529963230

    if message.chat.id == YOUR_CHAT_ID:
        await state.set_state(WaitForMessage.waiting)
        await message.reply("Ну давай кобылка, скидуй свое фото, оно отправитя всем:")

    else:
        await message.reply("Соси")


@photo_chat_all_router.message(WaitForMessage.waiting, F.photo)
async def handle_next_photo(message: types.Message, state: FSMContext):
    if message.caption and message.caption == "/stop":
        await message.reply("Щегол")
        await state.clear()
        return

    await message.reply("Щаааа")

    try:
        photo = message.photo[-1]

        photo_file = await bot.download(photo)

        async with AsyncSessionLocal() as session:
            group_ids = await get_all_group_ids(session)
            for group in group_ids:
                chat_id = group["chat_id"]
                group_name = group["group_name"]
                try:
                    await bot.send_photo(
                        chat_id=chat_id,
                        photo=types.BufferedInputFile(
                            photo_file.read(),
                            filename=f"schedule_{group_name}.jpg"
                        ),
                        caption=message.caption
                    )
                    print(f"Фото отправлено в {group_name} (chat_id: {chat_id})")
                except Exception as e:
                    print(f"Ошибка при отправке фото для {group_name}: {str(e)}")
    except Exception as e:
        print(f"Общая ошибка: {str(e)}")
    finally:
        await state.clear()