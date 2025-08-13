import asyncio
from datetime import datetime, time, timedelta
from aiogram import Router, types, F
from Database.db import Database
from pars import download_and_generate_schedule
from create_bot import bot
import os

get_photo_router = Router()


@get_photo_router.message(F.text == '14888841')
async def get_photo(message: types.Message = None):
    print("Команда '28733' получена")
    db = Database()
    await download_and_generate_schedule()
    try:
        start_time = datetime.now()
        async with db:
            group_ids = await db.get_all_group_ids()
            for group in group_ids:
                chat_id = group["chat_id"]
                group_name = group["group_name"]

                script_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(script_dir, "..", "output", f"{group_name}.png")

                file_path = os.path.normpath(file_path)

                today = datetime.now()
                tomorrow = today + timedelta(days=1)
                caption = tomorrow.strftime("%d.%m.%Y")

                print(file_path)
                try:
                    await bot.send_photo(chat_id, types.FSInputFile(file_path), caption=caption)
                    print(f"Расписание для группы {group_name} отправлено в чат {chat_id}.")
                except Exception as e:
                    print(f"Ошибка при отправке расписания для группы {group_name}: {e}")
    except Exception as e:
        print(f"Ошибка при получении данных из базы: {e}")
    finally:
        execution_time = datetime.now() - start_time
        print(f"Время выполнения: {execution_time}")

async def run_scheduler():
    """Запуск планировщика."""
    while True:
        await scheduled_task()
