from aiogram import Bot, Dispatcher, types
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

storage=MemoryStorage()

# инициализация бота
bot = Bot(token=os.getenv("TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()
