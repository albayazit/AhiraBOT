# запуск экземпляра бота
# переход на вебхуки
from aiogram import executor
from create_bot import dp
from handlers import client, other
from database import sqlite_bd
from create_bot import scheduler
from codes_script import scrap_codes
from food_script import scrap_food

client.register_handlers_client(dp)
# в самом низу во избежания нарушения логики
other.register_handlers_other(dp)

# функция при старте
async def on_startup(_):
    print('Бот запущен!')
    sqlite_bd.sql_start()
    client.schedule_jobs()
    await scrap_codes()
    await scrap_food()
    

# поллинг
if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)

