import asyncio
from datetime import datetime, time, timedelta
from app.services.pars import download_and_generate_schedule


async def run_parser_at(target_hour: int, target_minute: int):
    print(f"ПЛАНИРОВЩИК ПАРСЕРА ЗАПУЩЕН. Время: {target_hour:02}:{target_minute:02}")

    target_time = time(target_hour, target_minute)

    while True:
        now = datetime.now()
        next_run = datetime.combine(now.date(), target_time)

        if now >= next_run:
            next_run += timedelta(days=1)

        wait_seconds = (next_run - now).total_seconds()

        print(f"Парсер: ждем {(wait_seconds // 3600):.0f}ч {((wait_seconds % 3600) // 60):.0f}м")

        await asyncio.sleep(wait_seconds)

        print("Запускаем парсер...")
        try:
            await download_and_generate_schedule()
            print("Парсинг завершен.")
        except Exception as e:
            print(f"Ошибка парсинга: {e}")

        await asyncio.sleep(60)
