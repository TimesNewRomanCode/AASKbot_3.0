import asyncio
from datetime import datetime, time, timedelta
from aiogram import types
from app.crud.aaskUser import get_all_group_ids
from app.core.database import AsyncSessionLocal
from app.services.pars import download_and_generate_schedule
from app.core.create_bot import bot
import os


async def try_download_until_success(retry_interval=600):
    attempt = 1
    while True:
        try:
            print(f"Попытка скачивания #{attempt}")
            await download_and_generate_schedule()
            print("Скачивание успешно завершено!")
            return True
        except Exception as e:
            print(f"Ошибка скачивания: {e}")
            print(f"Следующая попытка через {retry_interval // 60} минут...")
            attempt += 1
            await asyncio.sleep(retry_interval)


async def send_schedules():
    start_time = datetime.now()
    try:
        async with AsyncSessionLocal() as session:
            group_ids = await get_all_group_ids(session)
            for group in group_ids:
                chat_id = group["chat_id"]
                group_name = group["group_name"]
                script_dir = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(
                    script_dir, "..", "output", f"{group_name}.png"
                )
                file_path = os.path.normpath(file_path)

                if not os.path.exists(file_path):
                    print(f"Файл не найден: {file_path}")
                    continue

                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
                caption = f"Расписание на {tomorrow}"

                try:
                    await bot.send_photo(
                        chat_id, types.FSInputFile(file_path), caption=caption
                    )
                    print(f"Расписание для {group_name} отправлено в чат {chat_id}")

                except Exception as e:
                    print(f"Ошибка отправки для {group_name}: {e}")

    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        execution_time = datetime.now() - start_time
        print(f"Время отправки: {execution_time}")


def get_next_valid_day(target_time):
    now = datetime.now()
    next_day = now + timedelta(days=1)

    while next_day.weekday() in [4, 5]:
        next_day += timedelta(days=1)

    next_valid_day = datetime.combine(next_day.date(), target_time)
    return next_valid_day


async def scheduled_task():
    print("ЗАПУСК ЗАДАЧИ РАСПИСАНИЯ")

    start_time_today = time(6, 0)
    now = datetime.now()

    # Проверяем, что бот инициализирован
    try:
        await bot.get_me()
    except Exception as e:
        print(f"Бот не инициализирован: {e}")
        await asyncio.sleep(60)
        return

    if now.weekday() in [4, 5]:
        next_valid_day = get_next_valid_day(start_time_today)
        wait_seconds = (next_valid_day - now).total_seconds()
        hours = int(wait_seconds // 3600)
        minutes = int((wait_seconds % 3600) // 60)
        print(f"Выходной день. Ожидание до {next_valid_day}: {hours:02}ч {minutes:02}м")
        await asyncio.sleep(wait_seconds)
        return

    if now.time() < start_time_today:
        next_run = datetime.combine(now.date(), start_time_today)
        wait_seconds = (next_run - now).total_seconds()
        print(
            f"Ожидание начала попыток скачивания: {wait_seconds // 3600:.0f}ч {(wait_seconds % 3600) // 60:.0f}м"
        )
        await asyncio.sleep(wait_seconds)

    print("Начинаем попытки скачивания...")
    await try_download_until_success()

    print("Скачивание успешно! Отправляем расписание...")
    await send_schedules()

    now_after_send = datetime.now()
    next_valid_day = get_next_valid_day(start_time_today)

    wait_seconds = (next_valid_day - now_after_send).total_seconds()
    hours = int(wait_seconds // 3600)
    minutes = int((wait_seconds % 3600) // 60)

    print(f"Расписание отправлено. Следующая попытка через {hours:02}ч {minutes:02}м")
    await asyncio.sleep(wait_seconds)


async def run_scheduler():
    # Даем время боту инициализироваться перед запуском планировщика
    await asyncio.sleep(10)

    while True:
        try:
            await scheduled_task()
        except Exception as e:
            print(f"Критическая ошибка в планировщике: {e}")
            await asyncio.sleep(3600)
