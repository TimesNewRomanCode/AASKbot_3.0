import asyncio
from datetime import datetime, time, timedelta
from aiogram import types
from aiogram.exceptions import TelegramForbiddenError
from sqlalchemy.orm import joinedload
import os

from app.keyboards.keyboards_Reply import verification
from app.models import User
from app.repositories import user_repository
from app.core.database import AsyncSessionLocal
from app.core.create_bot import bot


async def send_schedules():
    start_time = datetime.now()
    users_found = 0
    users_not_found = 0

    try:
        async with AsyncSessionLocal() as session:
            users = await user_repository.get_all(
                session,
                filter_criteria=User.is_active,
                custom_options=(joinedload(User.group),),
            )

            for user in users:
                today = datetime.now()
                target_day = today + timedelta(days=1)
                day_month = int(target_day.strftime("%d%m"))

                # Упрощенный путь к файлу
                file_path = f"./app/grop_photo/ААСК/{day_month}/{user.group_name}.png"
                file_path = os.path.normpath(file_path)

                if not os.path.exists(file_path):
                    print(f"Файл не найден: {file_path}")
                    users_not_found += 1
                    continue

                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
                caption = f"Расписание на {tomorrow}"

                try:
                    kb = verification()
                    await bot.send_photo(
                        user.chat_id,
                        types.FSInputFile(file_path),
                        caption=caption,
                        reply_markup=kb
                    )
                    print(f"Расписание для {user.group_name} отправлено в чат {user.chat_id}")
                    users_found += 1

                except Exception as e:
                    if isinstance(e, TelegramForbiddenError):
                        user.is_active = False
                        await session.commit()
                    print(f"Ошибка отправки для {user.group_name}: {e}")

    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        execution_time = datetime.now() - start_time
        print(f"Отправлено: {users_found}, Не найдено: {users_not_found}, Время: {execution_time}")

    return users_found > 0  # Возвращаем True если хотя бы одному пользователю отправили


async def try_send_until_success(retry_interval=600):
    """Пытается отправить расписание пока не получится"""
    attempt = 1
    while True:
        print(f"Попытка отправки расписания #{attempt}")

        success = await send_schedules()

        if success:
            print("Расписание успешно отправлено!")
            return True

        print(f"Файлы расписания не найдены. Следующая попытка через {retry_interval // 60} минут...")
        attempt += 1
        await asyncio.sleep(retry_interval)


def get_next_valid_day(target_time):
    now = datetime.now()
    next_day = now + timedelta(days=1)

    while next_day.weekday() in [4, 5]:  # Пятница и суббота
        next_day += timedelta(days=1)

    next_valid_day = datetime.combine(next_day.date(), target_time)
    return next_valid_day


async def scheduled_task():
    print("ЗАПУСК ЗАДАЧИ РАСПИСАНИЯ")

    start_time_today = time(6, 0)
    now = datetime.now()

    try:
        await bot.get_me()
    except Exception as e:
        print(f"Бот не инициализирован: {e}")
        await asyncio.sleep(60)
        return

    # Проверяем выходные
    if now.weekday() in [4, 5]:
        next_valid_day = get_next_valid_day(start_time_today)
        wait_seconds = (next_valid_day - now).total_seconds()
        hours = int(wait_seconds // 3600)
        minutes = int((wait_seconds % 3600) // 60)
        print(f"Выходной день. Ожидание до {next_valid_day}: {hours:02}ч {minutes:02}м")
        await asyncio.sleep(wait_seconds)
        return

    # Ждем времени начала
    if now.time() < start_time_today:
        next_run = datetime.combine(now.date(), start_time_today)
        wait_seconds = (next_run - now).total_seconds()
        print(f"Ожидание начала отправки: {wait_seconds // 3600:.0f}ч {(wait_seconds % 3600) // 60:.0f}м")
        await asyncio.sleep(wait_seconds)

    print("Начинаем попытки отправки расписания...")
    await try_send_until_success()

    # Планируем следующую задачу
    now_after_send = datetime.now()
    next_valid_day = get_next_valid_day(start_time_today)

    wait_seconds = (next_valid_day - now_after_send).total_seconds()
    hours = int(wait_seconds // 3600)
    minutes = int((wait_seconds % 3600) // 60)

    print(f"Расписание отправлено. Следующая отправка через {hours:02}ч {minutes:02}м")
    await asyncio.sleep(wait_seconds)


async def run_scheduler():
    await asyncio.sleep(10)
    while True:
        try:
            await scheduled_task()
        except Exception as e:
            print(f"Критическая ошибка в планировщике: {e}")
            await asyncio.sleep(3600)