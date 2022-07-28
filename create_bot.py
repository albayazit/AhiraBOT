from aiogram import Bot, Dispatcher, types
from config import TOKEN

# инициализация бота
# logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
