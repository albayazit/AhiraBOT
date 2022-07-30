from aiogram import Bot, Dispatcher, types
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

# инициализация бота
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
