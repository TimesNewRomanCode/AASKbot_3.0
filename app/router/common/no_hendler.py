from aiogram import Router, types, F
from app.keyboards.keyboards_Inline import get_inline_kb
from sqlalchemy.ext.asyncio import AsyncSession

no_hendler_router = Router()


@no_hendler_router.message(F.text == "Нет")
async def message_handler(message: types.Message, session: AsyncSession):
    await message.answer(
        "Ничего страшного, ещё раз", reply_markup=types.ReplyKeyboardRemove()
    )

    kb = await get_inline_kb(session)
    await message.answer("Из какой вы группы?", reply_markup=kb)
