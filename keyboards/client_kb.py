from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from parcer import parcer_exel
from datetime import date, timedelta, datetime
from database import sqlite_bd

#--------------------Buttons--------------------#

# time
button_time = KeyboardButton('🕦 Время намаза')
# tutor
button_tutor = KeyboardButton('🕌 Обучение')
button_tutor_what = KeyboardButton('❓\n Что такое намаз')
button_tutor_time = KeyboardButton('🕦\n Время намазов')
button_tutor_cond = KeyboardButton('❗\n Условия намаза')
button_tutor_gusl = KeyboardButton('🚿\n Гусль')
button_tutor_taharat = KeyboardButton('💧\n Тахарат')
button_tutor_forma = KeyboardButton('🧎\n Форма совершения намаза')
button_tutor_sura = KeyboardButton('📃\n Суры и дуа намаза')
button_tutor_women = KeyboardButton('🧕\n Женский намаз')
# audio
button_audio = KeyboardButton('🎧 Аудио')
button_audio_koran = KeyboardButton('📕\n Коран')
button_audio_hutba = KeyboardButton('📢\n Проповедь')
# books
button_books = KeyboardButton('📚 Книги')
# hadis
button_hadis = KeyboardButton('📖 Хадисы')
# dua
button_dua = KeyboardButton('🤲 Дуа')
# zikr
button_zikr = KeyboardButton('📿 Зикр')
# tracker
button_tracker = KeyboardButton('📈 Трекер')
# help
button_info = KeyboardButton('❗ Помощь')
# calendar
button_calendar = KeyboardButton('📅 Календарь')
# back
button_back = KeyboardButton('⏪ Назад')

# tatarstan inline
back_tat = InlineKeyboardButton('⏪ Назад', callback_data='back_tat')
next_tat = InlineKeyboardButton('Далее ⏩', callback_data='next_tat')

# Zikr
zikr_1 = InlineKeyboardButton('Салават', callback_data= 'zikr_1')
zikr_2 = InlineKeyboardButton('Дуа за родителей', callback_data= 'zikr_2')
zikr_3 = InlineKeyboardButton('Калима Тавхид', callback_data='zikr_3')
zikr_4 = InlineKeyboardButton('Субханаллаһи ва бихамдиһи',callback_data='zikr_4')
zikr_5 = InlineKeyboardButton('Аллаһумма иннака `афуун...', callback_data='zikr_5')
zikr_6 = InlineKeyboardButton('Астагфируллаһ аль Азыйм', callback_data='zikr_6')
zikr_7 = InlineKeyboardButton('Аят "Аль-Курси"', callback_data='zikr_7')
zikr_8 = InlineKeyboardButton('Ля хауля уа ляя куввата илляя билляһ', callback_data='zikr_8')
zikr_9 = InlineKeyboardButton('Хасбуналлаһу ва ни`маль вакиль', callback_data='zikr_9')
zikr_10 = InlineKeyboardButton('Субханаллаһ валь хамдулилляһ', callback_data='zikr_10')
zikr_11 = InlineKeyboardButton('Ля иляһа илля анта субханака', callback_data='zikr_11')
zikr_12 = InlineKeyboardButton('Ля иляха илляллаһу вахдаху ля шарика ляһ', callback_data='zikr_12')
zikr_13 = InlineKeyboardButton('Дуа "Кунут"', callback_data='zikr_13')
zikr_14 = InlineKeyboardButton('Раббана атина фи-д-дунья', callback_data='zikr_14')
zikr_15 = InlineKeyboardButton('Аллаһумма а`инни `аля зикрика', callback_data='zikr_15')
zikr_16 = InlineKeyboardButton('Таравих тасбих', callback_data='zikr_16')
zikr_17 = InlineKeyboardButton('Без категории', callback_data='zikr_17')

# calculate schools
school_1 = InlineKeyboardButton('Ханафитский', callback_data='school_1')
school_2 = InlineKeyboardButton('Шафиитский/Маликитский/Ханбалитский и др.', callback_data='school_0')

#--------------------Markups--------------------#

# main
markup_main = ReplyKeyboardMarkup()
markup_main.add(button_time).add(
    button_tracker, button_audio, button_books, button_hadis, button_dua, button_zikr, button_tutor, button_info, button_calendar
)

# city_add
inline_namaz_time = InlineKeyboardMarkup()
inline_namaz_time.add(InlineKeyboardButton('Татарстан', callback_data='tatarstan')).add(InlineKeyboardButton('Другой регион', callback_data='other_region'))

# learn
markup_namaz_tutor = ReplyKeyboardMarkup()
markup_namaz_tutor.add(
    button_tutor_what, button_tutor_time, button_tutor_cond, button_tutor_gusl, button_tutor_taharat, button_tutor_forma, button_tutor_sura, button_tutor_women, button_back
)

# audio
markup_audio = ReplyKeyboardMarkup()
markup_audio.add(
    button_audio_koran, button_audio_hutba
).add(button_back)

# zikr 
inline_zikr_all = InlineKeyboardMarkup()
inline_zikr_all.row_width = 2
inline_zikr_all.add(zikr_1, zikr_2, zikr_3, zikr_4, zikr_5, zikr_6, zikr_7, zikr_8, zikr_9, zikr_10, zikr_11, zikr_12, zikr_13, zikr_14, zikr_15, zikr_16, zikr_17)

# schools for other region
markup_school = InlineKeyboardMarkup()
markup_school.add(school_1).add(school_2)

# tatarstan cities
async def inline_namaz_time_tat(page):
	last_page = False
	markup = InlineKeyboardMarkup(row_width=2)
	keys = page*10
	for i in range(keys-10, keys):
		try:
			markup.insert(InlineKeyboardButton(parcer_exel.all_cities[i], callback_data=parcer_exel.all_cities[i]))
		except:
			if page != 1:
				last_page = True
				markup.add(back_tat)
				break
	if page == 1 and last_page == False:
		markup.add(next_tat)
	elif last_page == False:
		markup.insert(back_tat)
		markup.insert(next_tat)
	return markup

# lower in current city
async def inline_city(period, current_city):
    inline_city = InlineKeyboardMarkup(row_width=3)
    if period == 'today':
        inline_city.insert(InlineKeyboardButton('На завтра', callback_data = 'tomorrow_time')).insert(InlineKeyboardButton('На месяц', callback_data='month_time'))
    elif period == 'tomorrow':
        inline_city.insert(InlineKeyboardButton('На сегодня', callback_data=current_city)).insert(InlineKeyboardButton('На месяц', callback_data='month_time'))
    return inline_city

# all days in month
async def inline_month():
	m = datetime.now().month
	y = datetime.now().year
	days = (date(y, m+1, 1) - date(y, m, 1)).days
	d1 = date(y, m, 1)
	d2 = date(y, m, days)
	d3 = d2 - d1
	days = [(d1 + timedelta(days=i)).strftime('%Y.%m.%d') for i in range(d3.days + 1)]

	count = 0
	markup = InlineKeyboardMarkup(row_width=3)
	for day in days:
		if count < 9:
			markup.insert(InlineKeyboardButton(day[9:], callback_data='tatarstan'+day))
		else:
			markup.insert(InlineKeyboardButton(day[8:], callback_data='tatarstan'+day))
		count += 1
	return markup

# lower for other region cities
async def other_inline(user_id, address, time):
	markup = InlineKeyboardMarkup()
	zero_check = True
	if time == 'today':
		markup.insert(InlineKeyboardButton('На завтра', callback_data='other_tomorrow')).insert(InlineKeyboardButton('На месяц', callback_data='other_month'))
	elif time == 'tomorrow':
		markup.insert(InlineKeyboardButton('На сегодня', callback_data='other_today')).insert(InlineKeyboardButton('На месяц', callback_data='other_month'))
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_other WHERE user_id == {user_id}').fetchall():
		if item[0].lower() == address.lower():
			zero_check = False
			markup.add(InlineKeyboardButton('Удалить из избранных', callback_data='other_delete'))
			break
	if zero_check == True:
			markup.add(InlineKeyboardButton('Добавить в избранное', callback_data='other_add'))
	return markup

	


# favorite cities
async def favorite_cities(user_id):
	markup = InlineKeyboardMarkup(row_width=2)
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_other WHERE user_id == {user_id}').fetchall():
		markup.insert(InlineKeyboardButton(item[0], callback_data='city_other_'+item[0]))
	markup.add(InlineKeyboardButton('Добавить город', callback_data='add_city'))
	return markup

# all days in months for other regions
async def inline_month_other():
	m = datetime.now().month
	y = datetime.now().year
	days = (date(y, m+1, 1) - date(y, m, 1)).days
	d1 = date(y, m, 1)
	d2 = date(y, m, days)
	d3 = d2 - d1
	days = [(d1 + timedelta(days=i)).strftime('%Y.%m.%d') for i in range(d3.days + 1)]

	count = 0
	markup = InlineKeyboardMarkup(row_width=3)
	for day in days:
		if count < 9:
			markup.insert(InlineKeyboardButton(day[9:], callback_data='other_'+day))
		else:
			markup.insert(InlineKeyboardButton(day[8:], callback_data='other_'+day))
		count += 1
	return markup