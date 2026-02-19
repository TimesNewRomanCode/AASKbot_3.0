from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from app.core.config import settings
from app.core.create_bot import bot
from app.keyboards.keyboards_Inline_for_address import get_inline_kb_for_address
from app.keyboards.keyboards_Inline_for_college import get_inline_kb_for_college
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.keyboards_Inline_for_group import get_inline_kb_for_group
from app.keyboards.menu import menu
from app.services.services_for_models.user import register_user

register_router = Router()


@register_router.message(CommandStart())
async def message_handler(message: types.Message, session: AsyncSession):
    kb = await get_inline_kb_for_college(session)
    await message.answer("Из какого вы колледжа?", reply_markup=kb)


@register_router.callback_query(F.data.startswith("college_"))
async def process_order_callback_for_college(
    callback_query: CallbackQuery, session: AsyncSession
):
    college_name = callback_query.data.split("_")[1]
    kb = await get_inline_kb_for_address(session, college_name)
    await callback_query.message.edit_text(
        text="Укажите адрес вашего колледжа:", reply_markup=kb
    )
    await callback_query.answer()


@register_router.callback_query(F.data.startswith("address_"))
async def process_order_callback_for_address(
    callback_query: CallbackQuery, session: AsyncSession
):
    address_name = callback_query.data.split("_")[1]
    kb = await get_inline_kb_for_group(session, address_name)
    await callback_query.message.edit_text(text="Из какой вы группы?", reply_markup=kb)
    await callback_query.answer()


@register_router.callback_query(F.data.startswith("btn_"))
async def process_order_callback_for_group(
    callback_query: CallbackQuery, session: AsyncSession
):
    group_name = callback_query.data.split("_")[1]
    if group_name:
        await register_user(
            session=session,
            chat_id=callback_query.from_user.id,
            group_name=group_name,
            username=callback_query.from_user.username or "unknown",
        )

        print("Новый пользователь", callback_query.from_user.username)
        await bot.send_message(
            chat_id=settings.YOUR_CHAT_ID,
            text=f"Новый пользователь @{callback_query.from_user.username}",
        )
        await callback_query.message.edit_text(
            text=f"Теперь вы будете получать расписание группы {group_name}, вы всегда можете отписаться от рассылки"
        )
        await callback_query.answer()
