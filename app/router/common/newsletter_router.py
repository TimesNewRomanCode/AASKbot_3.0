from aiogram import Router, F
from aiogram.types import CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.user import newsletter_false_for_user

newsletter_router = Router()

@newsletter_router.callback_query(F.data == "newsletter_of")
async def newsletter(callback_query: CallbackQuery, session: AsyncSession):
    chat_id = callback_query.message.chat.id
    await callback_query.answer()
    await newsletter_false_for_user(session, chat_id)
    await callback_query.message.answer("Вы отписались от рассылки расписания")