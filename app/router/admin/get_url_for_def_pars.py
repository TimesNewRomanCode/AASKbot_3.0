from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import os
from dotenv import load_dotenv

from app.services.pars import download_and_generate_schedule

load_dotenv()

get_url_router = Router()


class WaitForGetUrl(StatesGroup):
    waiting = State()


@get_url_router.message(Command("get_url"))
async def message_chat(message: types.Message, state: FSMContext):
    YOUR_CHAT_ID = os.getenv("YOUR_CHAT_ID")
    YOUR_CHAT_ID = int(YOUR_CHAT_ID)

    if message.chat.id == YOUR_CHAT_ID:
        await state.set_state(WaitForGetUrl.waiting)
        await message.reply("Напиши правильный адрес рассписания:")

    else:
        await message.reply("Соси")


@get_url_router.message(WaitForGetUrl.waiting, F.text)
async def handle_next_message(message: types.Message, state: FSMContext):
    user_message = message.text
    if user_message == "/stop":
        await message.reply("Щегол")
        await state.clear()
    else:
        manual_url = user_message
        await download_and_generate_schedule(manual_url)
        await state.clear()
