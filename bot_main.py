# запуск экземпляра бота
from aiogram import executor
from create_bot import dp
from handlers import client, other
from database import sqlite_bd

client.register_handlers_client(dp)
# в самом низу во избежания нарушения логики
other.register_handlers_other(dp)

# функция при старте
async def on_startup(_):
    print('Бот запущен!')
    sqlite_bd.sql_start()

# поллинг
if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True, on_startup=on_startup)
