from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import user_repository


async def newsletter_of(
    session: AsyncSession, user_id: str
) -> types.InlineKeyboardMarkup:
    user = await user_repository.get_by_chat_id(session, user_id)
    if user.is_newsletter:
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Отписаться от рассылки", callback_data="newsletter_of"
                    )
                ]
            ]
        )
    else:
        return types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Подписаться на рассылки", callback_data="newsletter_yes"
                    )
                ]
            ]
        )
