from asyncio.windows_events import NULL
from tkinter import INSERT
from aiogram import Dispatcher, types
from create_bot import dp
from keyboards import client_kb
from parcer import parcer_dagestan, parcer_kazakhstan, parcer_other, parcer_tatarstan
from handlers import other
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import sqlite_bd
from datetime import datetime
import asyncio
from create_bot import scheduler, bot

# FSM
class FSMaddress(StatesGroup):
	address = State()
	school = State()

class FSMtracker(StatesGroup):
	fajr = State()
	zuhr = State()
	asr = State()
	magrib = State()
	isha = State()
	vitr = State()
	first_date = State()
	second_date = State()

# max message length
MESS_MAX_LENGTH = 4096
# по умолчанию
current_city = 'Казань'
# months
months = {
	'1':'Январь',
	'2':'Февраль',
	'3':'Март',
	'4':'Апрель',
	'5':'Май',
	'6':'Июнь',
	'7':'Июль',
	'8':'Август',
	'9':'Сентябрь',
	'10':'Октябрь',
	'11':'Ноябрь',
	'12':'Декабрь'
}

zikrs = {
	'1':'Салават',
	'2':'Дуа за родителей',
	'3':'Калима Тавхид',
	'4':'Субханаллаһи ва бихамдиһи',
	'5':'Аллаһумма иннака `афуун...',
	'6':'Дуа "Кунут"',
	'7':'Аят "Аль-Курси"',
	'8':'Ля хауля уа ляя куввата илляя билляһ',
	'9':'Хасбуналлаһу ва ни`маль вакиль',
	'10':'Субханаллаһ валь хамдулилляһ',
	'11':'Ля иляха илляллаһу вахдаху ля шарика ляһ',
	'12':'Ля иляһа илля анта субханака',
	'13':'Раббана атина фи-д-дунья',
	'14':'Аллаһумма а`инни `аля зикрика',
	'15':'Таравих тасбих',
	'16':'Без категории',
}

zikr_id = {
	'1':'AgACAgIAAxkBAAIj-2MEqww_R8l4yTihKS9V95GzPv0kAAJ4wDEbbjwoSP9h0ZMpyD2bAQADAgADeQADKQQ',
	'2':'AgACAgIAAxkBAAIj_WMEqxP4-QfrbN0aU5znSZFZlHKhAAJ5wDEbbjwoSNLXeYDXqzGXAQADAgADeQADKQQ',
	'3':'AgACAgIAAxkBAAIj_2MEqx1v7YWepWaOdjq8b_x5eKGqAAJ6wDEbbjwoSDeCXPTR4APQAQADAgADeQADKQQ',
	'4':'AgACAgIAAxkBAAIkAWMEqye9RmwmP_x4G5i_XR0hbc3LAAJ7wDEbbjwoSNbM0lZv1qe8AQADAgADeQADKQQ',
	'5':'AgACAgIAAxkBAAIkA2MEqyyFWVYrigrzR9GkjaJNOtIZAAJ8wDEbbjwoSHuWKaAJkTYdAQADAgADeQADKQQ',
	'6':'AgACAgIAAxkBAAIkBWMEqzS2JRpSdiaIO7Yn98RUznbQAAJ9wDEbbjwoSPgwgN7uLjQWAQADAgADeQADKQQ',
	'7':'AgACAgIAAxkBAAIkB2MEqzofTHX2EvshZ2sk8-Ehf1rvAAJ-wDEbbjwoSJDb9PGGvUs3AQADAgADeAADKQQ',
	'8':'AgACAgIAAxkBAAIkCWMEqz_eLurs9GC9Pxszd_BGwxxIAAJ_wDEbbjwoSF1sp6Wn4OMCAQADAgADeQADKQQ',
	'9':'AgACAgIAAxkBAAIkC2MEq0QZMppnDWP48U72P86n-t51AAKAwDEbbjwoSCHikcX1VGvrAQADAgADeQADKQQ',
	'10':'AgACAgIAAxkBAAIkDWMEq0mG7dzy9WkON0gX5nhfZNifAAKBwDEbbjwoSKDKheWQBGIeAQADAgADeQADKQQ',
	'11':'AgACAgIAAxkBAAIkD2MEq03iR7j_TmYbUiM7DraRblRYAAKCwDEbbjwoSArz1Oa4zOW6AQADAgADeQADKQQ',
	'12':'AgACAgIAAxkBAAIkEWMEq1FqrpMYczi_f4a1ClBR4OcsAAKDwDEbbjwoSFNW39f-yMXaAQADAgADeQADKQQ',
	'13':'AgACAgIAAxkBAAIkE2MEq3DkQ1k3gFWEAAG1on9nE78CAgAChMAxG248KEhWOZN02HeNTAEAAwIAA3kAAykE',
	'14':'AgACAgIAAxkBAAIkFWMEq3irb4oF_CH0CgJ98mzaI6ojAAKFwDEbbjwoSCVKzJIjoxsTAQADAgADeQADKQQ',
	'15':'AgACAgIAAxkBAAIkF2MEq4ONMSge7gwMoyTfLj8PBTp5AAKGwDEbbjwoSMACx-2DW3wpAQADAgADeQADKQQ',
	'16':'Без категории',
}

#--------------------Functions--------------------#

# Main keyboard | /start
async def start_command(message: types.Message):
	await message.answer('السلام عليكم ورحمة الله وبركاته', reply_markup=client_kb.markup_main)


# Favorite cities | 'Время намаза' (reply)
async def favorite_command(message: types.Message):
	global user_id
	user_id = message.from_user.id
	await message.answer('<b>Избранные города:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await client_kb.favorite_cities(user_id))

# Add new city | 'Добавить город' (inline)
async def time_command(callback : types.CallbackQuery):
	await callback.message.edit_text('Время намаза для других регионов сделана на основе наиболее предпочтительного метода вычитывания времени для данного города. Такие расчеты не всегда могут быть точными, убедительная просьба самостоятельно проверять наступление намаза по признакам при выборе "Другой регион".\n<b>Выберите регион:</b> ', reply_markup=client_kb.inline_namaz_time)
	await callback.answer()

# Tatarstan cities | 'Татарстан' (inline)
async def tatarstan_command(callback : types.CallbackQuery):
	global tat_page
	tat_page = 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def tatarstan_next(callback : types.CallbackQuery):
	global tat_page
	tat_page += 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

async def tatarstan_back(callback : types.CallbackQuery):
	global tat_page
	tat_page -= 1
	await callback.message.edit_text('Выберите Ваш <b>населенный пункт:</b> ', reply_markup=await client_kb.inline_namaz_time_tat(tat_page))
	await callback.answer()

# Tracker | 'Трекер'  (Reply)
async def tracker_command(message: types.Message):
	user_id = message.from_user.id
	info = sqlite_bd.cur.execute(f'SELECT EXISTS(SELECT * FROM tracker WHERE user_id == ?)', (user_id, ))
	if info.fetchone()[0] == 0:
		await message.answer('<b>Выберите способ:</b>', reply_markup=client_kb.markup_tracker_menu)
	else:
		await message.answer('Восстановление намазов:', reply_markup = await client_kb.markup_tracker(user_id))

async def tracker_myself(callback: types.CallbackQuery):
	await FSMtracker.fajr.set()
	await callback.message.delete()
	await callback.message.answer('Напишите количество <b>фаджр</b> намазов:', reply_markup = types.ReplyKeyboardRemove())
	await callback.answer()

async def tracker_fajr_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['fajr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.zuhr.set()
	await message.answer('Напишите количество <b>зухр</b> намазов: ')

async def tracker_zuhr_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['zuhr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.asr.set()
	await message.answer('Напишите количество <b>аср</b> намазов: ')

async def tracker_asr_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['asr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.magrib.set()
	await message.answer('Напишите количество <b>магриб</b> намазов: ')

async def tracker_magrib_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['magrib_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.isha.set()
	await message.answer('Напишите количество <b>иша</b> намазов: ')

async def tracker_isha_get(message: types.Message, state = FSMContext):
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['isha_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	await FSMtracker.vitr.set()
	await message.answer('Напишите количество <b>витр</b> намазов (при желании, можно написать 0): ')

async def tracker_vitr_get(message: types.Message, state = FSMContext):
	user_id = message.from_user.id
	async with state.proxy() as data:
		try:
			num = int(message.text)
			if num < 1:
				await state.finish()
				return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
			else:
				pass
			data['vitr_need'] = message.text
		except:
			await state.finish()
			return await message.answer('Некорректный формат. Напишите число больше 0', reply_markup = client_kb.markup_tracker_menu)
	async with state.proxy() as data:
		sqlite_bd.cur.execute('INSERT INTO tracker VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, NULL, data['fajr_need'], NULL, data['zuhr_need'], NULL, data['asr_need'], NULL, data['magrib_need'], NULL, data['isha_need'], NULL,data['vitr_need'], NULL, NULL))
		sqlite_bd.base.commit()
	await state.finish()
	await message.answer('Секундочку...', reply_markup = client_kb.markup_main)
	reply = await client_kb.markup_tracker(user_id)
	await asyncio.sleep(1)
	await message.answer('Восстановление намазов:', reply_markup = reply)

async def tracker_calculate(callback: types.CallbackQuery):
	await FSMtracker.first_date.set()
	await callback.message.delete()
	await callback.message.answer('Введите период, в течении которого нужно восстановить намазы.\nПервая дата: (формат: день.месяц.год)', reply_markup=types.ReplyKeyboardRemove())
	await callback.answer()

async def tracker_get_first(message: types.Message, state = FSMContext):
	try:
		async with state.proxy() as data:
			data['first_date'] = datetime.strptime(message.text, "%d.%m.%Y")
	except:
		await state.finish()
		return await message.answer('Неправильный формат!', reply_markup=client_kb.markup_main)
	await FSMtracker.second_date.set()
	await message.answer('Введите вторую дату:') 

async def tracker_get_second(message: types.Message, state = FSMContext):
	user_id = message.from_user.id
	try:
		async with state.proxy() as data:
			data['second_date'] = datetime.strptime(message.text, "%d.%m.%Y")
			first_date = data['first_date']
			second_date = data['second_date']
			result = (first_date - second_date).days
			if result < 0:
				result = result * -1 
			if first_date == second_date:
				await state.finish()
				return await message.answer('Даты не должны совпадать!', reply_markup=client_kb.markup_main)
			sqlite_bd.cur.execute('INSERT INTO tracker VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, NULL, result, NULL, result, NULL, result, NULL, result, NULL, result, NULL, result, second_date, first_date))
			sqlite_bd.base.commit()
	except:
		await state.finish()
		return await message.answer('Неправильный формат!', reply_markup=client_kb.markup_main)
	await state.finish()
	await message.answer('Добавить витр-намаз?', reply_markup=client_kb.markup_tracker_vitr)

async def tracker_vitr_get(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	if callback.data[5:] == 'no':
		sqlite_bd.cur.execute('UPDATE tracker SET vitr_need == ? WHERE user_id == ?', (0, user_id))
		sqlite_bd.base.commit()
	else:
		pass
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('Рассчитываю...', reply_markup = client_kb.markup_main)
	reply = await client_kb.markup_tracker(user_id)
	await asyncio.sleep(1)
	await callback.message.answer('Восстановление намазов:', reply_markup = reply)
	

async def tracker_reset(message: types.Message):
	await message.answer('Вы уверены, что хотите сбросить значения трекера?', reply_markup=client_kb.markup_tracker_reset)

async def tracker_reset_cancel(callback: types.CallbackQuery):
	await callback.message.edit_text('Операция отменена!')
	await callback.answer()

async def tracker_reset_yes(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		sqlite_bd.cur.execute(f'DELETE FROM tracker WHERE user_id == {user_id}')
		sqlite_bd.base.commit()
		await callback.message.delete()
		await callback.message.answer('Трекер сброшен успешно!', reply_markup=client_kb.markup_main)
	except:
		await callback.message.delete()
		await callback.message.answer('Трекер уже сброшен!', reply_markup=client_kb.markup_main)
	await callback.answer()

async def tracker_plus(callback: types.CallbackQuery):
	salat = callback.data[5:]
	user_id = callback.from_user.id
	if salat == 'fajr':
		sqlite_bd.cur.execute('UPDATE tracker SET fajr == (fajr + ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'zuhr':
		sqlite_bd.cur.execute('UPDATE tracker SET zuhr == (zuhr + ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'asr':
		sqlite_bd.cur.execute('UPDATE tracker SET asr == (asr + ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'magrib':
		sqlite_bd.cur.execute('UPDATE tracker SET magrib == (magrib + ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'isha':
		sqlite_bd.cur.execute('UPDATE tracker SET isha == (isha + ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	else: 
		sqlite_bd.cur.execute('UPDATE tracker SET vitr == (vitr + ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	await callback.message.edit_text('Восстановление намазов:', reply_markup = await client_kb.markup_tracker(user_id))
	await callback.answer()
	
async def tracker_minus(callback: types.CallbackQuery):
	salat = callback.data[6:]
	user_id = callback.from_user.id
	if salat == 'fajr':
		if sqlite_bd.cur.execute('SELECT fajr FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET fajr == (fajr - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'zuhr':
		if sqlite_bd.cur.execute('SELECT zuhr FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET zuhr == (zuhr - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'asr':
		if sqlite_bd.cur.execute('SELECT asr FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET asr == (asr - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'magrib':
		if sqlite_bd.cur.execute('SELECT magrib FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET magrib == (magrib - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	elif salat == 'isha':
		if sqlite_bd.cur.execute('SELECT isha FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET isha == (isha - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	else:
		if sqlite_bd.cur.execute('SELECT vitr FROM tracker WHERE user_id == ?', (user_id, )).fetchone()[0] == '0':
			await callback.answer()
			return await callback.message.answer('Значение не может быть ниже 0!')
		sqlite_bd.cur.execute('UPDATE tracker SET vitr == (vitr - ?) WHERE user_id == ?', (1, user_id))
		sqlite_bd.base.commit()
	await callback.message.edit_text('Восстановление намазов:', reply_markup = await client_kb.markup_tracker(user_id))
	await callback.answer()

async def other_btn_tracker(callback: types.CallbackQuery):
	data = callback.data[6:]
	await callback.answer()
	if data == 'salat':
		return await callback.message.answer('Название намаза')
	elif data == 'current':
		return await callback.message.answer('Число восстановленных намазов')
	else:
		return await callback.message.answer('Число необходимых намазов')

# learn | 'Обучение намазу' (Reply)
async def tutor_command(message: types.Message):
  await message.answer('Обучение на основе Ханафитского мазхаба.\nВыберите раздел: ', reply_markup=client_kb.markup_namaz_tutor)
# buttons in learn | (inline)
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


# Audio | 'Аудио' (Reply)
async def audio_command(message: types.Message):
    await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_audio)

async def audio_koran_menu(callback: types.CallbackQuery):
	await callback.message.edit_text('Выберите чтеца:')

async def audio_propoved_menu(callback: types.CallbackQuery):
	await callback.message.edit_text('Выберите проповедника:')


# Books | 'Книги' (Reply)
async def books_command(message: types.Message):
    await message.answer('Книги')


# Calendar | 'Календарь' (Reply)
async def calendar_command(message: types.Message):
	user_id = message.from_user.id
	await message.answer(await other.calendar_message(user_id))


# Info | 'Помощь' (Reply)
async def info_command(message: types.Message):
    await message.answer(other.info_message)


# Zikr | 'Зикр' (Reply)
async def zikr_command(message: types.Message):
	user_id = message.from_user.id
	try: 
		sqlite_bd.cur.execute('SELECT user_id FROM zikr WHERE user_id == ?', (user_id, )).fetchone()[0] == user_id
	except:
		sqlite_bd.cur.execute('INSERT INTO zikr VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (user_id, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL))
		sqlite_bd.base.commit()
	await message.answer('Выберите зикр: ', reply_markup=client_kb.inline_zikr_all)

async def send_message(dp: Dispatcher):
	sqlite_bd.cur.execute('UPDATE zikr SET zikr_1_today == "0", zikr_2_today == "0", zikr_3_today == "0", zikr_4_today == "0", zikr_5_today == "0", zikr_6_today == "0", zikr_7_today == "0", zikr_8_today == "0", zikr_9_today == "0", zikr_10_today == "0", zikr_11_today == "0", zikr_12_today == "0", zikr_13_today == "0", zikr_14_today == "0", zikr_15_today == "0", zikr_16_today == "0"')
	sqlite_bd.base.commit()

def schedule_jobs():
	scheduler.add_job(send_message, "interval", days=1, args=(dp, ))

async def zikr_get(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	text = callback.data[5:]
	await callback.answer()
	global zikr
	if text == '1':
		zikr = 1
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIj-2MEqww_R8l4yTihKS9V95GzPv0kAAJ4wDEbbjwoSP9h0ZMpyD2bAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_1_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_1_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(1))
	elif text == '2':
		zikr = 2
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIj_WMEqxP4-QfrbN0aU5znSZFZlHKhAAJ5wDEbbjwoSNLXeYDXqzGXAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_2_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_2_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(2))
	elif text == '3':
		zikr = 3
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIj_2MEqx1v7YWepWaOdjq8b_x5eKGqAAJ6wDEbbjwoSDeCXPTR4APQAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_3_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_3_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(3))
	elif text == '4':
		zikr = 4
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkAWMEqye9RmwmP_x4G5i_XR0hbc3LAAJ7wDEbbjwoSNbM0lZv1qe8AQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_4_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_4_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(4))
	elif text == '5':
		zikr = 5
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkA2MEqyyFWVYrigrzR9GkjaJNOtIZAAJ8wDEbbjwoSHuWKaAJkTYdAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_5_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_5_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(5))
	elif text == '6':
		zikr = 6
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkBWMEqzS2JRpSdiaIO7Yn98RUznbQAAJ9wDEbbjwoSPgwgN7uLjQWAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_6_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_6_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(6))
	elif text == '7':
		zikr = 7
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkB2MEqzofTHX2EvshZ2sk8-Ehf1rvAAJ-wDEbbjwoSJDb9PGGvUs3AQADAgADeAADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_7_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_7_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(7))
	elif text == '8':
		zikr = 8
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkCWMEqz_eLurs9GC9Pxszd_BGwxxIAAJ_wDEbbjwoSF1sp6Wn4OMCAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_8_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_8_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(8))
	elif text == '9':
		zikr = 9
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkC2MEq0QZMppnDWP48U72P86n-t51AAKAwDEbbjwoSCHikcX1VGvrAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_9_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_9_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(9))
	elif text == '10':
		zikr = 10
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkDWMEq0mG7dzy9WkON0gX5nhfZNifAAKBwDEbbjwoSKDKheWQBGIeAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_10_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_10_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(10))
	elif text == '11':
		zikr = 11
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkD2MEq03iR7j_TmYbUiM7DraRblRYAAKCwDEbbjwoSArz1Oa4zOW6AQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_11_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_11_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(11))
	elif text == '12':
		zikr = 12
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkEWMEq1FqrpMYczi_f4a1ClBR4OcsAAKDwDEbbjwoSFNW39f-yMXaAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_12_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_12_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(12))
	elif text == '13':
		zikr = 13
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkE2MEq3DkQ1k3gFWEAAG1on9nE78CAgAChMAxG248KEhWOZN02HeNTAEAAwIAA3kAAykE', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_13_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_13_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(13))
	elif text == '14':
		zikr = 14
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkFWMEq3irb4oF_CH0CgJ98mzaI6ojAAKFwDEbbjwoSCVKzJIjoxsTAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_14_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_14_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(14))
	elif text == '15':
		zikr = 15
		await callback.message.delete()
		await bot.send_photo(callback.from_user.id, 'AgACAgIAAxkBAAIkF2MEq4ONMSge7gwMoyTfLj8PBTp5AAKGwDEbbjwoSMACx-2DW3wpAQADAgADeQADKQQ', caption=f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_15_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_15_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(15))
	else:
		zikr = 16
		await callback.message.edit_text(f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_16_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_16_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup= client_kb.markup_zikr_lower(16))

async def zikr_plus(callback: types.CallbackQuery):
	data = callback.data[10:]
	user_id = callback.from_user.id
	sqlite_bd.cur.execute(f'UPDATE zikr SET zikr_{data}_today == zikr_{data}_today + 1, zikr_{data}_all == zikr_{data}_all + 1 WHERE user_id == ?', (user_id, ))
	sqlite_bd.base.commit()
	await callback.answer()
	await callback.message.edit_caption(f'Сегодня: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup= await client_kb.markup_zikr_lower(data))

async def zikr_reset(callback: types.CallbackQuery):
	data = callback.data[11:]
	await callback.message.answer(f'Вы уверены, что хотите сбросить зикр "{zikrs[data]}"?', reply_markup=await client_kb.markup_zikr_reset(data))
	await callback.answer()

async def zikr_reset_cancel(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	data = callback.data[18:]
	if data == '16':
		await callback.message.answer(f'Сегодня: {sqlite_bd.cur.execute("SELECT zikr_16_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute("SELECT zikr_16_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup= client_kb.markup_zikr_lower(16))
	else:
		await bot.send_photo(callback.from_user.id, zikr_id[data], caption=f'Сегодня: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_today FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]} ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ \nЗа все время: {sqlite_bd.cur.execute(f"SELECT zikr_{data}_all FROM zikr WHERE user_id == ?", (user_id, )).fetchone()[0]}', reply_markup=await client_kb.markup_zikr_lower(data))
	await callback.answer()

async def zikr_reset_yes(callback: types.CallbackQuery):
	data = callback.data[15:]
	user_id = callback.from_user.id
	try:
		sqlite_bd.cur.execute(f'UPDATE zikr SET zikr_{data}_all == "0", zikr_{data}_today == "0" WHERE user_id == ?', (user_id, ))
		sqlite_bd.base.commit()
		await callback.answer()
		await callback.message.delete()
		await callback.message.answer('Зикр успешно сброшен!')
	except:
		await callback.answer()
		await callback.message.delete()
		await callback.message.answer('Произошла ошибка!')

async def zikr_all(callback: types.CallbackQuery):
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('Выберите зикр: ', reply_markup=client_kb.inline_zikr_all)

# Unknown messages
async def help_command(message: types.Message):
	await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_main)


# back button
async def back_command(message: types.Message):
    await message.answer('Выберите раздел: ', reply_markup=client_kb.markup_main)


# today time for tatarstan
async def namaz_day_command(callback : types.CallbackQuery):
	user_id = callback.from_user.id
	global current_city
	current_city = callback.data
	await callback.message.edit_text(await parcer_tatarstan.get_time(current_city, 'today'), reply_markup = await client_kb.inline_city('today', current_city, user_id))
	await callback.answer()


# tomorrow time for tatarstan
async def next_day_time_command(callback : types.CallbackQuery):
	user_id = callback.from_user.id
	global current_city
	await callback.message.edit_text(await parcer_tatarstan.get_time(current_city, 'tomorrow'), reply_markup = await client_kb.inline_city('tomorrow', current_city, user_id))
	await callback.answer()

# all days in month for tatarstan
async def month_time_command(callback : types.CallbackQuery):
	await callback.message.edit_text(f'Город: <b>{current_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await client_kb.inline_month())
	await callback.answer()
#--------------------Get new other city--------------------#
# first message
async def address_add(callback: types.CallbackQuery):
	global user_id
	user_id = callback.from_user.id
	await FSMaddress.address.set()
	await callback.message.delete()
	await callback.message.answer('Напишите название города', reply_markup=types.ReplyKeyboardRemove())
	await callback.answer()

async def cancel_handler(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.answer('Действие отменено ❌', reply_markup=client_kb.markup_main)

# check address
async def address_get(message: types.message, state=FSMContext):
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_other WHERE user_id == {user_id}').fetchall():
		if item[0].lower() == message.text.lower():
			await state.finish()
			return await message.answer('Город с таким названием уже есть в избранных!', reply_markup = client_kb.markup_main)
	try:
		await parcer_other.city_check(message.text)
		await message.answer('Город найден! ✅', reply_markup=client_kb.markup_main)
	except:
		await state.finish()
		return await message.answer('Такого города не нашлось, проверьте название!', reply_markup = client_kb.markup_main)
	async with state.proxy() as data:
		data['address'] = message.text
	await FSMaddress.school.set()
	await message.answer('<b>Выберите мазхаб:</b>', reply_markup=client_kb.markup_school)
# school
async def school_get(callback: types.CallbackQuery, state=FSMContext):
	global address, school
	user_id = callback.from_user.id
	async with state.proxy() as data:
		data['school'] = callback.data[7]
		address = data['address']
		school = data['school']
	time = await parcer_other.get_day_time(state)
	await callback.answer()
	msg = await callback.message.edit_text('Секундочку...')
	await asyncio.sleep(1)
	await msg.edit_text(time, reply_markup=await client_kb.other_inline(user_id, address, 'today'))
	await state.finish()
# time from menu for other regions

async def time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global address
	address = str(callback.data[11:])
	try:
		await callback.message.edit_text(await parcer_other.get_day_time_from_menu(user_id, str(callback.data[11:])),reply_markup=await client_kb.other_inline(user_id, str(callback.data[11:]), 'today'))
	except:
		await callback.message.edit_text('Что-то пошло не так, повторите попытку!')
	await callback.answer()

async def favorite_add_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('INSERT INTO favorite_other VALUES (?, ?, ?)', (user_id, address, school))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def favorite_delete_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('DELETE FROM favorite_other WHERE user_id == ? AND address == ?', (user_id, address))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def month_days_other(callback: types.CallbackQuery):
	await callback.message.edit_text(f'Город: <b>{address}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b> ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',reply_markup=await client_kb.inline_month_other())
	await callback.answer()

async def tomorrow_time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address))
	except:
		on_db = False
	await callback.message.edit_text(await parcer_other.get_calendar_time(address, datetime.now().day + 1, school), reply_markup=await client_kb.other_inline(user_id, address, 'tomorrow'))
	await callback.answer()

async def today_time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address))
	except:
		on_db = False
	await callback.message.edit_text(await parcer_other.get_calendar_time(address, datetime.now().day, school), reply_markup=await client_kb.other_inline(user_id, address, 'today'))
	await callback.answer()

async def month_time_other(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	try:
		school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address))
	except:
		on_db = False
	day = callback.data[11:]
	await callback.message.edit_text(await parcer_other.get_calendar_time(address, day, school), reply_markup=await client_kb.other_inline(user_id, address, 'month'))
	await callback.answer()

async def tatarstan_month(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	await callback.message.edit_text(await parcer_tatarstan.get_time(current_city,callback.data[15:]), reply_markup=await client_kb.inline_city('tomorrow', current_city, user_id))
	await callback.answer()
	await callback.answer()

async def tatarstan_favorite_add(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute(f'INSERT INTO favorite_tatarstan VALUES (?, ?)', (user_id, current_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def tatarstan_favorite_delete(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('DELETE FROM favorite_tatarstan WHERE user_id == ? AND address == ?', (user_id, current_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def dagestan_menu(callback: types.CallbackQuery):
	global dag_page
	dag_page = 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()
async def dagestan_menu_next(callback: types.CallbackQuery):
	global dag_page
	dag_page += 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()
async def dagestan_menu_back(callback: types.CallbackQuery):
	global dag_page
	dag_page -= 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.dagestan_markup(dag_page))
	await callback.answer()

async def dagestan_today_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	dag_city = callback.data[9:]
	await callback.message.edit_text(await parcer_dagestan.get_day_time(dag_city), reply_markup= await client_kb.dag_city(dag_city, 'today',user_id))
	await callback.answer()

async def dagestan_tomorrow_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	await callback.message.edit_text(await parcer_dagestan.get_tomorrow_time(dag_city), reply_markup= await client_kb.dag_city(dag_city, 'tomorrow',user_id))
	await callback.answer()

async def dagestan_month(callback: types.CallbackQuery):
	global dag_city
	await callback.message.edit_text(f'Город: <b>{dag_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',reply_markup=await client_kb.dagestan_month())
	await callback.answer()

async def dagestan_month_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	await callback.message.edit_text(await parcer_dagestan.get_month_time(dag_city, callback.data[9:]), reply_markup= await client_kb.dag_city(dag_city, 'month', user_id))
	await callback.answer()

async def dagestan_favorite_add(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global daz_city
	sqlite_bd.cur.execute(f'INSERT INTO favorite_dagestan VALUES (?, ?)', (user_id, dag_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def dagestan_favorite_delete(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global dag_city
	sqlite_bd.cur.execute('DELETE FROM favorite_dagestan WHERE user_id == ? AND address == ?', (user_id, dag_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def kazakhstan_menu(callback: types.CallbackQuery):
	global kaz_page
	kaz_page = 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()
async def kazakhstan_menu_next(callback: types.CallbackQuery):
	global kaz_page
	kaz_page += 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()
async def kazakhstan_menu_back(callback: types.CallbackQuery):
	global kaz_page
	kaz_page -= 1
	await callback.message.edit_text('<b>Выберите населенный пункт:</b>', reply_markup=await client_kb.kazakhstan_markup(kaz_page))
	await callback.answer()

async def kazakhstan_today_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	kaz_city = callback.data[9:]
	await callback.message.edit_text(await parcer_kazakhstan.get_day_time(kaz_city), reply_markup=await client_kb.kaz_city(kaz_city, 'today', user_id))
	await callback.answer()

async def kazakhstan_tomorrow_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	await callback.message.edit_text(await parcer_kazakhstan.get_tomorrow_time(kaz_city), reply_markup=await client_kb.kaz_city(kaz_city, 'tomorrow', user_id))
	await callback.answer()

async def kazakhstan_month(callback: types.CallbackQuery):
	global kaz_city
	await callback.message.edit_text(f'Город: <b>{kaz_city}</b>\nМесяц: <b>{months[str(datetime.now().month)]}</b>\n<b>Выберите день:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',reply_markup=await client_kb.kazakhstan_month())
	await callback.answer()

async def kazakhstan_month_time(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	await callback.message.edit_text(await parcer_kazakhstan.get_month_time(kaz_city, callback.data[9:]), reply_markup= await client_kb.kaz_city(kaz_city, 'month', user_id))
	await callback.answer()

async def kazakhstan_favorite_add(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	global kaz_city
	sqlite_bd.cur.execute(f'INSERT INTO favorite_kazakhstan VALUES (?, ?)', (user_id, kaz_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Добавлено в избранные ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()

async def kazakhstan_favorite_delete(callback: types.CallbackQuery):
	global kaz_city
	user_id = callback.from_user.id
	sqlite_bd.cur.execute('DELETE FROM favorite_kazakhstan WHERE user_id == ? AND address == ?', (user_id, kaz_city))
	sqlite_bd.base.commit()
	await callback.message.edit_text('Удалено из избранных ✅', reply_markup = client_kb.markup_favorite)
	await callback.answer()
	
async def favorite_cities(callback: types.CallbackQuery):
	user_id = callback.from_user.id
	await callback.message.edit_text('<b>Избранные города:</b>ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await client_kb.favorite_cities(user_id))
	await callback.answer()

async def photo_id(message: types.Message):
	await message.answer(f"Id: {message.photo[2].file_id}")
# dispatcher
def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(start_command, commands=['start'])
	dp.register_message_handler(favorite_command, lambda message: message.text == "🕦 Время намаза")
	dp.register_message_handler(tracker_command, lambda message: message.text == "📈 Трекер")
	dp.register_message_handler(tracker_reset, commands=['reset'])
	dp.register_callback_query_handler(tracker_reset_cancel, text = 'tracker_cancel')
	dp.register_callback_query_handler(tracker_reset_yes, text = 'tracker_reset')
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
	dp.register_callback_query_handler(namaz_day_command, text = parcer_tatarstan.all_cities)
	dp.register_callback_query_handler(next_day_time_command, text = 'tomorrow_time')
	dp.register_callback_query_handler(tatarstan_command, text = 'tatarstan')
	dp.register_callback_query_handler(tatarstan_next, text = 'next_tat')
	dp.register_callback_query_handler(tatarstan_back, text = 'back_tat')
	dp.register_callback_query_handler(month_time_command, text = 'month_time')
	dp.register_callback_query_handler(address_add, text = 'other_region')
	dp.register_message_handler(cancel_handler, commands='cancel', state='*')
	dp.register_message_handler(address_get, state=FSMaddress.address)
	dp.register_callback_query_handler(school_get, text_startswith='school_',state=FSMaddress.school)
	dp.register_callback_query_handler(favorite_add_other, text='other_add')
	dp.register_callback_query_handler(favorite_delete_other, text='other_delete')
	dp.register_callback_query_handler(time_other, text_startswith='city_other_')
	dp.register_callback_query_handler(month_days_other, text='other_month')
	dp.register_callback_query_handler(tomorrow_time_other, text='other_tomorrow')
	dp.register_callback_query_handler(today_time_other, text='other_today')
	dp.register_callback_query_handler(month_time_other, text_startswith='other_days_')
	dp.register_callback_query_handler(tatarstan_month, text_startswith='tatarstan_days_')
	dp.register_callback_query_handler(tatarstan_favorite_add, text='tatarstan_favorite_add')
	dp.register_callback_query_handler(tatarstan_favorite_delete, text='tatarstan_favorite_delete')
	dp.register_callback_query_handler(dagestan_menu, text = 'dagestan')
	dp.register_callback_query_handler(kazakhstan_menu, text = 'kazakhstan')
	dp.register_callback_query_handler(kazakhstan_menu_next, text = 'next_kaz')
	dp.register_callback_query_handler(kazakhstan_menu_back, text = 'back_kaz')
	dp.register_callback_query_handler(kazakhstan_today_time, text_startswith = 'kaz_city_')
	dp.register_callback_query_handler(kazakhstan_tomorrow_time, text = 'kaz_tomorrow')
	dp.register_callback_query_handler(kazakhstan_month, text = 'kaz_month')
	dp.register_callback_query_handler(kazakhstan_month_time, text_startswith = 'kaz_days_')
	dp.register_callback_query_handler(kazakhstan_favorite_add, text='kaz_add')
	dp.register_callback_query_handler(kazakhstan_favorite_delete, text='kaz_delete')
	dp.register_callback_query_handler(dagestan_menu_next, text = 'next_dag')
	dp.register_callback_query_handler(dagestan_menu_back, text = 'back_dag')
	dp.register_callback_query_handler(dagestan_today_time, text_startswith = 'dag_city_')
	dp.register_callback_query_handler(dagestan_tomorrow_time, text = 'dag_tomorrow')
	dp.register_callback_query_handler(dagestan_month, text = 'dag_month')
	dp.register_callback_query_handler(dagestan_month_time, text_startswith='dag_days_')
	dp.register_callback_query_handler(dagestan_favorite_add, text = 'dag_add')
	dp.register_callback_query_handler(dagestan_favorite_delete, text = 'dag_delete')
	dp.register_callback_query_handler(favorite_cities, text = 'favorite_cities')
	dp.register_callback_query_handler(tracker_myself, text = 'tracker_myself')
	dp.register_message_handler(tracker_fajr_get, state = FSMtracker.fajr)
	dp.register_message_handler(tracker_zuhr_get, state = FSMtracker.zuhr)
	dp.register_message_handler(tracker_asr_get, state = FSMtracker.asr)
	dp.register_message_handler(tracker_magrib_get, state = FSMtracker.magrib)
	dp.register_message_handler(tracker_isha_get, state = FSMtracker.isha)
	dp.register_message_handler(tracker_vitr_get, state = FSMtracker.vitr)
	dp.register_callback_query_handler(tracker_plus, text_startswith = 'plus_')
	dp.register_callback_query_handler(tracker_minus, text_startswith = 'minus_')
	dp.register_callback_query_handler(other_btn_tracker, text_startswith = 'troth_')
	dp.register_callback_query_handler(tracker_calculate, text = 'tracker_calculate')
	dp.register_message_handler(tracker_get_first, state = FSMtracker.first_date)
	dp.register_message_handler(tracker_get_second, state = FSMtracker.second_date)	
	dp.register_callback_query_handler(tracker_vitr_get, text_startswith = 'vitr_')
	dp.register_callback_query_handler(zikr_reset_cancel, text_startswith = 'zikr_reset_cancel_')
	dp.register_callback_query_handler(zikr_reset_yes, text_startswith = 'zikr_reset_yes_')
	dp.register_callback_query_handler(zikr_reset, text_startswith = 'zikr_reset_')
	dp.register_callback_query_handler(zikr_plus, text_startswith = 'zikr_plus_')
	dp.register_callback_query_handler(zikr_all, text = 'zikr_all')
	dp.register_callback_query_handler(zikr_get, text_startswith = 'zikr_')

	dp.register_message_handler(photo_id, content_types=["photo"])
