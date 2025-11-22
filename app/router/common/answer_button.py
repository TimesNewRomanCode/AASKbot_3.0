from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import register_user

answer_button_router = Router()


@answer_button_router.callback_query(F.data.startswith("btn_"))
async def process_order_callback(callback_query: CallbackQuery, session: AsyncSession):
    group_name = callback_query.data.split("_")[1]
    if group_name:
        await register_user(
            session=session,
            chat_id=callback_query.from_user.id,
            group_name=group_name,
            username=callback_query.from_user.username or "unknown",
        )
        print("Новый пользователь", callback_query.from_user.username)
        await callback_query.message.edit_text(
            text=f"Ваша группа {group_name}?",
        )
        await callback_query.answer()
