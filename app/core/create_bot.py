from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from os import getenv

# from Database.db import Database
from dotenv import load_dotenv

from app.core.config import settings


bot = Bot(token=getenv(settings.BOT_TOKEN), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(storage=MemoryStorage())

# db = Database()
