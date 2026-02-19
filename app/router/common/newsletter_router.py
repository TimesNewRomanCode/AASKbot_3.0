

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.is_newsletter_keyboards import newsletter_of
from app.services.services_for_models.user import newsletter_false_for_user, newsletter_true_for_user

newsletter_router = Router()


@newsletter_router.callback_query(F.data.startswith("newsletter_of"))
async def newsletter_toggle(call: CallbackQuery, session: AsyncSession):
    chat_id = call.message.chat.id
    await newsletter_false_for_user(session, chat_id)

    user_id = str(call.message.chat.id)
    new_keyboard = await newsletter_of(session, user_id)

    await call.message.edit_reply_markup(reply_markup=new_keyboard)

    await call.answer()


@newsletter_router.callback_query(F.data.startswith("newsletter_yes"))
async def newsletter_toggle(call: CallbackQuery, session: AsyncSession):

    chat_id = call.message.chat.id
    await newsletter_true_for_user(session, chat_id)

    user_id = str(call.message.chat.id)
    new_keyboard = await newsletter_of(session, user_id)

    await call.message.edit_reply_markup(reply_markup=new_keyboard)

    await call.answer()


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

