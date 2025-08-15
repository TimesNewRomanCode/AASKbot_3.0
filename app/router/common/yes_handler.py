from aiogram import Router, F, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.aaskUser import register_user

yes_handler_router = Router()

@yes_handler_router.message(F.text == 'Да')
async def yes(message: types.Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    group_name = data.get("group_name")
    if group_name:
        await register_user(
            session=session,
            chat_id=message.chat.id,
            group_name=group_name,
            username=message.from_user.username or "unknown"
        )
        await message.answer(
            f"Теперь вы будете получать расписание своей группы {group_name}",
            reply_markup=ReplyKeyboardRemove()
        )
