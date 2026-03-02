import asyncio
import logging

from app.keyboards.commands import set_commands
from app.services.get_photo import run_scheduler
from app.core.create_bot import bot, dp
from app.router.common import (
    newsletter_router,
    schedule_manager,
    register_router,
    schedule_manager_by_group
)
from app.router.admin import (
    message_chat_all_router,
    photo_chat_all_router,
    get_url_router,
)
from app.core.database import get_session
from app.middlewares.db import DbSessionMiddleware
from app.services.services_for_parsing.pars_aag import parse_aag
from app.services.services_for_parsing.pars_aask import parse_aask
from app.services.services_for_parsing.starting_parsers import run_parser_at


async def main():
    print("Запуск бота...")

    dp.message.middleware(DbSessionMiddleware(get_session))
    dp.callback_query.middleware(DbSessionMiddleware(get_session))

    dp.include_routers(
        register_router,
        message_chat_all_router,
        photo_chat_all_router,
        schedule_manager,
        get_url_router,
        newsletter_router,
        schedule_manager_by_group,
    )
    await set_commands(bot)
    parser_task = asyncio.create_task(run_parser_at(5, 30))
    polling_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.sleep(3)
    await parse_aag.run()
    await parse_aask.download_and_generate_schedule()
    scheduler_task = asyncio.create_task(run_scheduler())

    await asyncio.gather(polling_task, parser_task, scheduler_task)
    await parse_aag.run()
    await parse_aask.download_and_generate_schedule()
    logging.info("Бот завершает работу.")
    await bot.delete_webhook(drop_pending_updates=True)
