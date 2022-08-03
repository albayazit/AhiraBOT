from cgitb import text
from aiogram import Dispatcher, types, Bot
from create_bot import dp
from keyboards import client_kb
from parcer import parcer_exel, parcer_hidjra, parcer_main
from handlers import other
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import sqlite_bd

# FSM
class FSMaddress(StatesGroup):
	address = State()
	method = State()
	school = State()

# макс. длина сообщения
MESS_MAX_LENGTH = 4096
# страница в инлайне Татарстана
tat_page = 1
# получение даты по хиджре
hidjra_date = parcer_hidjra.main()
# выбранный город, по умолчанию Казань
current_city = 'Казань'

# стартовые кнопки, реакция на /start
async def start_command(message: types.Message):
    await message.answer('السلام عليكم ورحمة الله وبركاته', reply_markup=client_kb.markup_main)


# кнопка времени намаза
async def favorite_command(message: types.Message):
		user_id = message.from_user.id
		await message.answer('<b>Избранные города:</b>', reply_markup=client_kb.favorite_cities(user_id))

async def time_command(callback : types.CallbackQuery):
    await callback.message.edit_text('Время намаза для других регионов сделана на основе расчетов Всемирной Исламской лиги, при наличии, ориентируйтесь на расчеты ДУМ Вашего региона.\n<b>Выберите регион:</b> ', reply_markup=client_kb.inline_namaz_time)


# кнопка трекер
async def tracker_command(message: types.Message):
    await message.answer('Это трекер')


# кнопка обучения намазу
async def tutor_command(message: types.Message):
    await message.answer('Обучение на основе Ханафитского мазхаба.\nВыберите раздел: ', reply_markup=client_kb.markup_namaz_tutor)
# кнопки обучений
async def tutor_namaz_command(message: types.Message):
    await message.answer(other.tut_namaz_message)

async def tutor_time_command(message: types.Message):
    await message.answer(other.tut_time_message)

async def tutor_cond_command(message: types.Message):
	for x in range(0, len(other.tut_cond_message), MESS_MAX_LENGTH - 1400):
		mess_tut = other.tut_cond_message[x: x + MESS_MAX_LENGTH - 1400] 
		await message.answer(mess_tut)

async def tutor_gusl_command(message: types.Message):
    await message.answer(other.tut_gusl_message)

async def tutor_taharat_command(message: types.Message):
    await message.answer(other.tut_taharat_message)

async def tutor_forma_command(message: types.Message):
	for x in range(0, len(other.tut_forma_message), MESS_MAX_LENGTH - 57):
		mess_form = other.tut_forma_message[x: x + MESS_MAX_LENGTH - 57] 
		await message.answer(mess_form)

async def tutor_sura_command(message: types.Message):
    await message.answer(other.tut_sura_message)

async def tutor_women_command(message: types.Message):
    await message.answer(other.tut_women_message)


# кнопка аудио
async def audio_command(message: types.Message):
    await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_audio)


# кнопка книг
async def books_command(message: types.Message):
    await message.answer('Книги')


# кнопка календаря
async def calendar_command(message: types.Message):
    await message.answer(other.calendar_message)


# кнопка информации
async def info_command(message: types.Message):
    await message.answer(other.info_message)


# кнопка зикра
async def zikr_command(message: types.Message):
    await message.answer('Выберите зикр: ', reply_markup=client_kb.inline_zikr_all)


# реакция на неожиданные сообщения
async def help_command(message: types.Message):
	await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_main)


# кнопка назад (переброс на стартовые кнопки)
async def back_command(message: types.Message):
    await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_main)


# время намаза на сегодня
async def namaz_day_command(callback : types.CallbackQuery):
	global current_city
	current_city = callback.data
	await callback.message.edit_text(parcer_exel.get_day_time(current_city), reply_markup = client_kb.inline_city('today', current_city))
	await callback.answer()


# Время на след. день
async def next_day_time_command(callback : types.CallbackQuery):
	global current_city
	await callback.message.edit_text(parcer_exel.get_nextday_time(current_city), reply_markup = client_kb.inline_city('tomorrow', current_city))
	await callback.answer()

# Время на месяц
async def month_time_command(callback : types.CallbackQuery):
	await callback.message.edit_text('<b>Выберите число:</b>', reply_markup=client_kb.inline_month())


# населенные пункты Татарстана inline-button
async def tatarstan_command(callback : types.CallbackQuery):
	global tat_page
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def tatarstan_next(callback : types.CallbackQuery):
	global tat_page
	tat_page += 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def tatarstan_back(callback : types.CallbackQuery):
	global tat_page
	tat_page -= 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def address_add(callback: types.CallbackQuery):
	await FSMaddress.address.set()
	await callback.message.edit_text('Напишите название города')
	await callback.answer()

async def address_get(message: types.message, state=FSMContext):
	try:
		await parcer_main.city_check(message.text)
	except:
		await state.finish()
		return await message.answer('Такого города не нашлось, проверьте название!')
	async with state.proxy() as data:
		data['address'] = message.text
	await FSMaddress.method.set()
	await message.answer('<b>Выберите метод расчета:</b>', reply_markup=client_kb.markup_method)

async def method_get(callback: types.CallbackQuery, state=FSMContext):
	async with state.proxy() as data:
		data['method'] = callback.data[7:]
	await FSMaddress.school.set()
	await callback.answer()
	await callback.message.edit_text('<b>Выберите мазхаб:</b>', reply_markup=client_kb.markup_school)

async def school_get(callback: types.CallbackQuery, state=FSMContext):
	global address, method, school
	user_id = callback.from_user.id
	async with state.proxy() as data:
		data['school'] = callback.data[7]
		address = data['address']
		method = data['method']
		school = data['school']
	await callback.answer()
	await callback.message.edit_text(await parcer_main.get_day_time(state), reply_markup=client_kb.other_inline(user_id, address))
	await state.finish()

async def time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	address = str(callback.data[11:])
	try:
		await callback.message.edit_text(await parcer_main.get_day_time_from_menu(user_id, str(callback.data[11:])),reply_markup=client_kb.other_inline(user_id, str(callback.data[11:])))
	except:
		await callback.message.edit_text('Что-то пошло не так, повторите попытку!')
	await callback.answer()

async def favorite_add_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('INSERT INTO favorite_other VALUES (?, ?, ?, ?)', (user_id, address, method, school))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅')
	await callback.answer()

async def favorite_delete_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('DELETE FROM favorite_other WHERE user_id == ? AND address == ?', (user_id, address))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅')
	await callback.answer()

# dispatcher
def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(start_command, commands=['start'])
	dp.register_message_handler(favorite_command, lambda message: message.text == "🕦 Время намаза")
	dp.register_message_handler(tracker_command, lambda message: message.text == "📈 Трекер")
	dp.register_message_handler(tutor_command, lambda message: message.text == "🕌 Обучение")
	dp.register_message_handler(tutor_namaz_command, lambda message: message.text == "❓\n Что такое намаз")
	dp.register_message_handler(tutor_time_command, lambda message: message.text == "🕦\n Время намазов")
	dp.register_message_handler(tutor_cond_command, lambda message: message.text == "❗\n Условия намаза")
	dp.register_message_handler(tutor_gusl_command, lambda message: message.text == "🚿\n Гусль")
	dp.register_message_handler(tutor_taharat_command, lambda message: message.text == "💧\n Тахарат")	
	dp.register_message_handler(tutor_forma_command, lambda message: message.text == "🧎\n Форма совершения намаза")	
	dp.register_message_handler(tutor_sura_command, lambda message: message.text == "📃\n Суры и дуа намаза")
	dp.register_message_handler(tutor_women_command, lambda message: message.text == "🧕\n Женский намаз")					
	dp.register_message_handler(audio_command, lambda message: message.text == "🎧 Аудио")
	dp.register_message_handler(books_command, lambda message: message.text == "📚 Книги")
	dp.register_message_handler(calendar_command, lambda message: message.text == "📅 Календарь")
	dp.register_message_handler(info_command, lambda message: message.text == "❗ Помощь")
	dp.register_message_handler(zikr_command, lambda message: message.text == "📿 Зикр")
	dp.register_message_handler(help_command, commands=['help'])
	dp.register_message_handler(back_command, lambda message: message.text == "⏪ Назад")
	dp.register_callback_query_handler(time_command, text = 'add_city')
	dp.register_callback_query_handler(namaz_day_command, text = parcer_exel.cities_exel)
	dp.register_callback_query_handler(next_day_time_command, text = 'tomorrow_time')
	dp.register_callback_query_handler(tatarstan_command, text = 'tatarstan')
	dp.register_callback_query_handler(tatarstan_next, text = 'next_tat')
	dp.register_callback_query_handler(tatarstan_back, text = 'back_tat')
	dp.register_callback_query_handler(month_time_command, text = 'month_time')
	dp.register_callback_query_handler(address_add, text = 'other_region')
	dp.register_message_handler(address_get, state=FSMaddress.address)
	dp.register_callback_query_handler(method_get, text_startswith='method_',state=FSMaddress.method)
	dp.register_callback_query_handler(school_get, text_startswith='school_',state=FSMaddress.school)
	dp.register_callback_query_handler(favorite_add_other, text='other_add')
	dp.register_callback_query_handler(favorite_delete_other, text='other_delete')
	dp.register_callback_query_handler(time_other, text_startswith='city_other_')
	