

from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.services_for_models.user import newsletter_false_for_user, newsletter_true_for_user

newsletter_router = Router()


@newsletter_router.message(Command("newsletter_no"))
async def newsletter_no(message: Message, session: AsyncSession):
    chat_id = message.chat.id
    await newsletter_false_for_user(session, chat_id)
    await message.answer("Вы отписались от рассылки расписания")

@newsletter_router.message(Command("newsletter_yes"))
async def newsletter_yes(message: Message, session: AsyncSession):
    chat_id = message.chat.id
    await newsletter_true_for_user(session, chat_id)
    await message.answer("Вы подписались на рассылку расписания")