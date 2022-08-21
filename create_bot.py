from aiogram import Bot, Dispatcher, types
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

storage=MemoryStorage()

# инициализация бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
scheduler = AsyncIOScheduler()
