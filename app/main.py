import asyncio
import logging
from app.services.get_photo import run_scheduler
from app.core.create_bot import bot, dp
from app.router.common import (
    start_router,
    answer_button_router,
)
from app.router.admin import message_chat_all_router, photo_chat_all_router
from app.core.database import get_session
from app.middlewares.db import DbSessionMiddleware


async def main():
    print("Запуск бота...")

    dp.message.middleware(DbSessionMiddleware(get_session))
    dp.callback_query.middleware(DbSessionMiddleware(get_session))

    dp.include_routers(
        start_router,
        answer_button_router,
        message_chat_all_router,
        photo_chat_all_router,
    )

    polling_task = asyncio.create_task(dp.start_polling(bot))
    scheduler_task = asyncio.create_task(run_scheduler())

    await asyncio.gather(polling_task, scheduler_task)

    logging.info("Бот завершает работу.")
    await bot.delete_webhook(drop_pending_updates=True)
