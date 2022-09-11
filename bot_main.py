# запуск экземпляра бота
# переход на вебхуки
from create_bot import dp, bot
from handlers import client, other
from database import sqlite_bd
from create_bot import scheduler
from codes_script import scrap_codes
from food_script import scrap_food
from aiogram.utils.executor import start_webhook
import config

client.register_handlers_client(dp)
# в самом низу во избежания нарушения логики
other.register_handlers_other(dp)

WEBHOOK_URL = f"{config.WEBHOOK_HOST}{config.WEBHOOK_PATH}"

# функция при старте
async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    print('Бот запущен!')
    sqlite_bd.sql_start()
    client.schedule_jobs()
    await scrap_codes()
    await scrap_food()

async def on_shutdown(dispatcher):
    await bot.delete_webhook()

# поллинг
if __name__ == '__main__':
    scheduler.start()
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        on_startup=on_startup,
        skip_updates=True,
        host = config.WEBAPP_HOST,
        port = config.WEBAPP_PORT
    )

