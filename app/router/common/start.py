from aiogram import Router, types
from aiogram.filters import CommandStart
from app.keyboards.keyboards_Inline import get_inline_kb
from sqlalchemy.ext.asyncio import AsyncSession

start_router = Router()

@start_router.message(CommandStart())
async def message_handler(message: types.Message, session: AsyncSession):
    kb = await get_inline_kb(session)
    await message.reply("Из какой вы группы?", reply_markup=kb)
