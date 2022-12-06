from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from parcer import parcer_tatarstan, parcer_dagestan, parcer_kazakhstan, parcer_hadis
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
button_koran = KeyboardButton('📖 30-й джуз')
# books
button_names = KeyboardButton('❾❾ Имён')
# hadis
button_hadis = KeyboardButton('📕 Хадисы')
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
# halal
button_halal = KeyboardButton('🍔 Халяль гид')
# e-codes
button_codes = KeyboardButton('📄 E-добавки')

button_all_tutor = KeyboardButton('⏪ Меню')



# Zikr
zikr_1 = InlineKeyboardButton('Салават', callback_data= 'zikr_1')
zikr_2 = InlineKeyboardButton('Дуа за родителей', callback_data= 'zikr_2')
zikr_3 = InlineKeyboardButton('Калима Тавхид', callback_data='zikr_3')
zikr_4 = InlineKeyboardButton('Субханаллаһи ва бихамдиһи',callback_data='zikr_4')
zikr_5 = InlineKeyboardButton('Аллаһумма иннака `афуун...', callback_data='zikr_5')
zikr_6 = InlineKeyboardButton('Дуа "Кунут"', callback_data='zikr_6')
zikr_7 = InlineKeyboardButton('Аят "Аль-Курси"', callback_data='zikr_7')
zikr_8 = InlineKeyboardButton('Ля хауля уа ляя куввата илляя билляһ', callback_data='zikr_8')
zikr_9 = InlineKeyboardButton('Хасбуналлаһу ва ни`маль вакиль', callback_data='zikr_9')
zikr_10 = InlineKeyboardButton('Субханаллаһ валь хамдулилляһ', callback_data='zikr_10')
zikr_11 = InlineKeyboardButton('Ля иляха илляллаһу вахдаху ля шарика ляһ', callback_data='zikr_11')
zikr_12 = InlineKeyboardButton('Ля иляһа илля анта субханака', callback_data='zikr_12')
zikr_13 = InlineKeyboardButton('Раббана атина фи-д-дунья', callback_data='zikr_13')
zikr_14 = InlineKeyboardButton('Аллаһумма а`инни `аля зикрика', callback_data='zikr_14')
zikr_15 = InlineKeyboardButton('Таравих тасбих', callback_data='zikr_15')
zikr_16 = InlineKeyboardButton('Без категории', callback_data='zikr_16')

# calculate schools
school_1 = InlineKeyboardButton('Ханафитский', callback_data='school_1')
school_2 = InlineKeyboardButton('Шафиитский/Маликитский/Ханбалитский и др.', callback_data='school_0')

qoran_78 = InlineKeyboardButton('«Ан-Наба»', callback_data='qoran_78')
qoran_79 = InlineKeyboardButton('«Назиʼат»', callback_data='qoran_79')
qoran_80 = InlineKeyboardButton('«’Абаса»', callback_data='qoran_80')
qoran_81 = InlineKeyboardButton('«Ат-Таквир»', callback_data='qoran_81')
qoran_82 = InlineKeyboardButton('«Аль-Инфитар»', callback_data='qoran_82')
qoran_83 = InlineKeyboardButton('«Аль-Мутаффифун»', callback_data='qoran_83')
qoran_84 = InlineKeyboardButton('«Аль-Иншикак»', callback_data='qoran_84')
qoran_85 = InlineKeyboardButton('«Аль-Бурудж»', callback_data='qoran_85')
qoran_86 = InlineKeyboardButton('«Ат-Торик»', callback_data='qoran_86')
qoran_87 = InlineKeyboardButton('«Аль-Аʼля»', callback_data='qoran_87')
qoran_88 = InlineKeyboardButton('«Аль-Гашия»', callback_data='qoran_88')
qoran_89 = InlineKeyboardButton('«Аль-Фаджр»', callback_data='qoran_89')
qoran_90 = InlineKeyboardButton('«Аль-Баляд»', callback_data='qoran_90')
qoran_91 = InlineKeyboardButton('«Аш-Шамс»', callback_data='qoran_91')
qoran_92 = InlineKeyboardButton('«Аль-Лейль»', callback_data='qoran_92')
qoran_93 = InlineKeyboardButton('«Ад-Духа»', callback_data='qoran_93')
qoran_94 = InlineKeyboardButton('«Аш-Шарх»', callback_data='qoran_94')
qoran_95 = InlineKeyboardButton('«Ат-Тин»', callback_data='qoran_95')
qoran_96 = InlineKeyboardButton('«Аль-ʼаляк»', callback_data='qoran_96')
qoran_97 = InlineKeyboardButton('«Аль-Кадр»', callback_data='qoran_97')
qoran_98 = InlineKeyboardButton('«Аль-Байина»', callback_data='qoran_98')
qoran_99 = InlineKeyboardButton('«Аль-Зальзаля»', callback_data='qoran_99')
qoran_100 = InlineKeyboardButton('«Аль-ʼадият»', callback_data='qoran_100')
qoran_101 = InlineKeyboardButton('«Аль-Кариʼа»', callback_data='qoran_101')
qoran_102 = InlineKeyboardButton('«Ат-Такасур»', callback_data='qoran_102')
qoran_103 = InlineKeyboardButton('«Аль-ʼАср»', callback_data='qoran_103')
qoran_104 = InlineKeyboardButton('«Аль-Хумаза»', callback_data='qoran_104')
qoran_105 = InlineKeyboardButton('«Аль-Филь»', callback_data='qoran_105')
qoran_106 = InlineKeyboardButton('«Аль-Курайш»', callback_data='qoran_106')
qoran_107 = InlineKeyboardButton('«Аль-Маʼун»', callback_data='qoran_107')
qoran_108 = InlineKeyboardButton('«Аль-Каусар»', callback_data='qoran_108')
qoran_109 = InlineKeyboardButton('«Аль-Кафирун»', callback_data='qoran_109')
qoran_110 = InlineKeyboardButton('«Ан-Наср»', callback_data='qoran_110')
qoran_111 = InlineKeyboardButton('«Аль-Масад»', callback_data='qoran_111')
qoran_112 = InlineKeyboardButton('«Аль-Ихлас»', callback_data='qoran_112')
qoran_113 = InlineKeyboardButton('«Аль-Фаляк»', callback_data='qoran_113')
qoran_114 = InlineKeyboardButton('«Ан-Нас»', callback_data='qoran_114')

surah_tafsir = {
	'114':'https://azan.ru/tafsir/an-nas',
	'113':'https://azan.ru/tafsir/al-falyak',
	'112':'https://azan.ru/tafsir/al-ihlas',
	'111':'https://azan.ru/tafsir/al-masad',
	'110':'https://azan.ru/tafsir/an-nasr',
	'109':'https://azan.ru/tafsir/al-kafirun',
	'108':'https://azan.ru/tafsir/al-kausar',
	'107':'https://azan.ru/tafsir/al-maun',
	'106':'https://azan.ru/tafsir/al-kupaysh',
	'105':'https://azan.ru/tafsir/al-fil',
	'104':'https://azan.ru/tafsir/al-humaza',
	'103':'https://azan.ru/tafsir/al-asr',
	'102':'https://azan.ru/tafsir/at-takasur',
	'101':'https://azan.ru/tafsir/al-karia',
	'100':'https://azan.ru/tafsir/al-adiyat',
	'99':'https://azan.ru/tafsir/az-zalzalya',
	'98':'https://azan.ru/tafsir/al-bayina',
	'97':'https://azan.ru/tafsir/al-kadr',
	'96':'https://azan.ru/tafsir/al-alyak',
	'95':'https://azan.ru/tafsir/at-tin',
	'94':'https://azan.ru/tafsir/ash-sharh',
	'93':'https://azan.ru/tafsir/ad-duha',
	'92':'https://azan.ru/tafsir/al-leyl',
	'91':'https://azan.ru/tafsir/ash-shams',
	'90':'https://azan.ru/tafsir/al-balyad',
	'89':'https://azan.ru/tafsir/al-fadzhr',
	'88':'https://azan.ru/tafsir/al-gashiya',
	'87':'https://azan.ru/tafsir/al-alya',
	'86':'https://azan.ru/tafsir/at-torik',
	'85':'https://azan.ru/tafsir/al-burudzh',
	'84':'https://azan.ru/tafsir/al-inshikak',
	'83':'https://azan.ru/tafsir/al-mutaffifun',
	'82':'https://azan.ru/tafsir/al-infitar',
	'81':'https://azan.ru/tafsir/at-takvir',
	'80':'https://azan.ru/tafsir/abasa',
	'79':'https://azan.ru/tafsir/naziat',
	'78':'https://azan.ru/tafsir/an-naba'
}

surah = {
	'114':'114 | Сура «Ан-Нас»',
	'113':'113 | Сура «Аль-Фаляк»',
	'112':'112 | Сура «Аль-Ихлас»',
	'111':'111 | Сура «Аль-Масад»',
	'110':'110 | Сура «Ан-Наср»',
	'109':'109 | Сура «Аль-Кафирун»',
	'108':'108 | Сура «Аль-Каусар»',
	'107':'107 | Сура «Аль-Ма’ун»',
	'106':'106 | Сура «Аль-Куpaйш»',
	'105':'105 | Сура «Аль-Филь»',
	'104':'104 | Сура «Аль-Хумаза»',
	'103':'103 | Сура «Аль-ʼАср»',
	'102':'102 | Сура «Ат-Такасур»',
	'101':'101 | Сура «Аль-Кариʼа»',
	'100':'100 | Сура «Аль-ʼадият»',
	'99':'99 | Сура «Аль-Зальзаля»',
	'98':'98 | Сура «Аль-Байина»',
	'97':'97 | Сура «Аль-Кадр»',
	'96':'96 | Сура «Аль-ʼаляк»',
	'95':'95 | Сура «Ат-Тин»',
	'94':'94 | Сура «Аш-Шарх»',
	'93':'93 | Сура «Ад-Духа»',
	'92':'92 | Сура «Аль-Лейль»',
	'91':'91 | Сура «Аш-Шамс»',
	'90':'90 | Сура «Аль-Баляд»',
	'89':'89 | Сура «Аль-Фаджр»',
	'88':'88 | Сура «Аль-Гашия»',
	'87':'87 | Сура «Аль-Аʼля»',
	'86':'86 | Сура «Ат-Торик»',
	'85':'85 | Сура «Аль-Бурудж»',
	'84':'84 | Сура «Аль-Иншикак»',
	'83':'83 | Сура «Аль-Мутаффифун»',
	'82':'82 | Сура «Аль-Инфитар»',
	'81':'81 | Сура «Ат-Таквир»',
	'80':'80 | Сура «’Абаса»',
	'79':'79 | Сура «Назиʼат»',
	'78':'78 | Сура «Ан-Наба»'
}

#--------------------Markups--------------------#

# main
markup_main = ReplyKeyboardMarkup()
markup_main.add(button_time).add(button_tracker, button_codes, button_koran, button_names, button_hadis, button_zikr, button_tutor, button_info, button_calendar)

# city_add
inline_namaz_time = InlineKeyboardMarkup()
inline_namaz_time.add(InlineKeyboardButton('Татарстан', callback_data='tatarstan')).add(InlineKeyboardButton('Дагестан', callback_data='dagestan')).add(InlineKeyboardButton('Казахстан', callback_data='kazakhstan')).add(InlineKeyboardButton('Другой регион', callback_data='other_region'))

# learn
markup_namaz_tutor = ReplyKeyboardMarkup()
markup_namaz_tutor.add(
    button_tutor_what, button_tutor_time, button_tutor_cond, button_tutor_gusl, button_tutor_taharat, button_tutor_forma, button_tutor_sura, button_tutor_women, button_back
)

markup_tutor_back = ReplyKeyboardMarkup(resize_keyboard=True)
markup_tutor_back.add(button_all_tutor)

# qoran
async def markup_qoran(page):
	markup = InlineKeyboardMarkup(row_width=2)
	if page == 1:
		for item in reversed(range(101, 115)):
			markup.insert(InlineKeyboardButton(surah[str(item)], callback_data='surah_'+str(item)))
	elif page == 2:
		for item in reversed(range(87, 101)):
			markup.insert(InlineKeyboardButton(surah[str(item)], callback_data='surah_'+str(item)))
	elif page == 3:
		for item in reversed(range(78, 87)):
			markup.insert(InlineKeyboardButton(surah[str(item)], callback_data='surah_'+str(item)))
		# markup.insert(InlineKeyboardButton('Все аудио', callback_data='qoran_audio_all'))
		markup.add(InlineKeyboardButton('⏪ Назад',  callback_data = 'qoran_back_'+str(page)))
		return markup
	if page == 1:
		markup.add(InlineKeyboardButton('Далее ⏩', callback_data = 'qoran_next_'+str(page)))
	else:
		markup.add(InlineKeyboardButton('⏪ Назад',  callback_data = 'qoran_back_'+str(page))).insert(InlineKeyboardButton('Далее ⏩', callback_data = 'qoran_next_'+str(page)))
	return markup

async def markup_surah(data):
	markup_surah = InlineKeyboardMarkup()
	markup_surah.insert(InlineKeyboardButton('Тафсир', url = surah_tafsir[str(data)])).insert(InlineKeyboardButton('Аудио', callback_data='qoran_audio_'+str(data))).insert(InlineKeyboardButton('Перевод', callback_data='surah_translate_'+str(data)))
	return markup_surah
	
# zikr 
inline_zikr_all = InlineKeyboardMarkup()
inline_zikr_all.row_width = 2
inline_zikr_all.add(zikr_1, zikr_2, zikr_3, zikr_4, zikr_5, zikr_6, zikr_7, zikr_8, zikr_9, zikr_10, zikr_11, zikr_12, zikr_13, zikr_14, zikr_15, zikr_16)

inline_zikr = InlineKeyboardMarkup()
inline_zikr.add(InlineKeyboardButton('Дуа пророков', callback_data='dua_prorokov')).insert(InlineKeyboardButton('Зикры', callback_data='zikr_all_get'))

async def markup_zikr_lower(zikr):
	markup = InlineKeyboardMarkup()
	markup.add(InlineKeyboardButton('+', callback_data='zikr_plus_'+str(zikr))).add(InlineKeyboardButton('Сбросить', callback_data='zikr_reset_'+str(zikr))).insert(InlineKeyboardButton('Зикры', callback_data='zikr_all'))
	if zikr == 16:
		pass
	else:
		markup.insert(InlineKeyboardButton('Польза', callback_data='zikr_polza_'+str(zikr)))
	return markup

async def markup_zikr_reset(zikr):
	markup = InlineKeyboardMarkup()
	markup.add(InlineKeyboardButton('Отмена', callback_data='zikr_reset_cancel_'+str(zikr))).insert(InlineKeyboardButton('Сбросить', callback_data='zikr_reset_yes_'+str(zikr)))
	return markup

# schools for other region
markup_school = InlineKeyboardMarkup()
markup_school.add(school_1).add(school_2)

markup_favorite = InlineKeyboardMarkup()
markup_favorite.add(InlineKeyboardButton('Избранные города', callback_data='favorite_cities'))

# tatarstan cities
async def inline_namaz_time_tat(page):
	last_page = False
	markup = InlineKeyboardMarkup(row_width=2)
	keys = page*10
	for i in range(keys-10, keys):
		try:
			markup.insert(InlineKeyboardButton(parcer_tatarstan.all_cities[i], callback_data=parcer_tatarstan.all_cities[i]))
		except:
			if page != 1:
				last_page = True
				markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_tat_'+str(page)))
				break
	if page == 1 and last_page == False:
		markup.add(InlineKeyboardButton('Далее ⏩', callback_data='next_tat_'+str(page)))
	elif last_page == False:
		markup.insert(InlineKeyboardButton('⏪ Назад', callback_data='back_tat_'+str(page)))
		markup.insert(InlineKeyboardButton('Далее ⏩', callback_data='next_tat_'+str(page)))
	return markup

# lower in current city tatarstan
async def inline_city(period, current_city, user_id):
	inline_city = InlineKeyboardMarkup(row_width=3)
	zero_check = True
	if period == 'today':
		inline_city.insert(InlineKeyboardButton('На завтра', callback_data = 'tomorrow_time')).insert(InlineKeyboardButton('На месяц', callback_data='month_time'))
	elif period == 'tomorrow':
		inline_city.insert(InlineKeyboardButton('На сегодня', callback_data=current_city)).insert(InlineKeyboardButton('На месяц', callback_data='month_time'))
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_tatarstan WHERE user_id == {user_id}').fetchall():
		if item[0] == current_city:
			zero_check = False
			inline_city.add(InlineKeyboardButton('Удалить из избранных', callback_data='tatarstan_favorite_delete'))
			break
	if zero_check == True:
		inline_city.add(InlineKeyboardButton('Добавить в избранные', callback_data='tatarstan_favorite_add'))
	return inline_city

	
# all days in month
async def inline_month():
	m = datetime.now().month
	y = datetime.now().year
	if m != 12:
		days = (date(y, m+1, 1) - date(y, m, 1)).days
	else:
		days = 31
	d1 = date(y, m, 1)
	d2 = date(y, m, days)
	d3 = d2 - d1
	days = [(d1 + timedelta(days=i)).strftime('%Y.%m.%d') for i in range(d3.days + 1)]

	count = 0
	markup = InlineKeyboardMarkup(row_width=5)
	for day in days:
		if count < 9:
			markup.insert(InlineKeyboardButton(day[9:], callback_data='tatarstan_days_'+day))
		else:
			markup.insert(InlineKeyboardButton(day[8:], callback_data='tatarstan_days_'+day))
		count += 1
	return markup

# lower for other region cities
async def other_inline(user_id, address, time):
	markup = InlineKeyboardMarkup()
	zero_check = True
	if time == 'today':
		markup.insert(InlineKeyboardButton('На завтра', callback_data='other_tomorrow')).insert(InlineKeyboardButton('На месяц', callback_data='other_month'))
	else:
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
	markup = InlineKeyboardMarkup(row_width=1)
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_tatarstan WHERE user_id == {user_id}').fetchall():
		markup.insert(InlineKeyboardButton(item[0], callback_data=item[0]))
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_dagestan WHERE user_id == {user_id}').fetchall():
		markup.insert(InlineKeyboardButton(item[0], callback_data='dag_city_'+item[0]))
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_kazakhstan WHERE user_id == {user_id}').fetchall():
		markup.insert(InlineKeyboardButton(item[0], callback_data='kaz_city_'+item[0]))
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
	markup = InlineKeyboardMarkup(row_width=5)
	for day in days:
		if count < 9:
			markup.insert(InlineKeyboardButton(day[9:], callback_data='other_days_'+day[9:]))
		else:
			markup.insert(InlineKeyboardButton(day[8:], callback_data='other_days_'+day[8:]))
		count += 1
	return markup

async def kazakhstan_markup(page):
	last_page = False
	markup = InlineKeyboardMarkup(row_width=2)
	keys = page*10
	for i in range(keys-10, keys):
		try:
			markup.insert(InlineKeyboardButton(parcer_kazakhstan.cities[i], callback_data='kaz_city_'+parcer_kazakhstan.cities[i]))
		except:
			if page != 1:
				last_page = True
				markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_kaz_'+str(page)))
				break
	if page == 1 and last_page == False:
		markup.add(InlineKeyboardButton('Далее ⏩', callback_data='next_kaz_'+str(page)))
	elif last_page == False:
		markup.insert(InlineKeyboardButton('⏪ Назад', callback_data='back_kaz_'+str(page)))
		markup.insert(InlineKeyboardButton('Далее ⏩', callback_data='next_kaz_'+str(page)))
	return markup

async def kaz_city(address, period, user_id):
	markup = InlineKeyboardMarkup()
	zero_check = True
	if period == 'today':
		markup.insert(InlineKeyboardButton('На завтра', callback_data='kaz_tomorrow')).insert(InlineKeyboardButton('На месяц', callback_data='kaz_month'))
	else:
		markup.insert(InlineKeyboardButton('На сегодня', callback_data='kaz_city_'+address)).insert(InlineKeyboardButton('На месяц', callback_data='kaz_month'))
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_kazakhstan WHERE user_id == {user_id}').fetchall():
		if item[0] == address:
			zero_check = False
			markup.add(InlineKeyboardButton('Удалить из избранных', callback_data='kaz_delete'))
			break
	if zero_check == True:
			markup.add(InlineKeyboardButton('Добавить в избранное', callback_data='kaz_add'))
	return markup

async def kazakhstan_month():
	m = datetime.now().month
	y = datetime.now().year
	days = (date(y, m+1, 1) - date(y, m, 1)).days
	d1 = date(y, m, 1)
	d2 = date(y, m, days)
	d3 = d2 - d1
	days = [(d1 + timedelta(days=i)).strftime('%Y.%m.%d') for i in range(d3.days + 1)]

	count = 0
	markup = InlineKeyboardMarkup(row_width=5)
	for day in days:
		if count < 9:
			markup.insert(InlineKeyboardButton(day[9:], callback_data='kaz_days_'+day[9:]))
		else:
			markup.insert(InlineKeyboardButton(day[8:], callback_data='kaz_days_'+day[8:]))
		count += 1
	return markup

async def dagestan_markup(page):
	last_page = False
	markup = InlineKeyboardMarkup(row_width=2)
	keys = page*10
	for i in range(keys-10, keys):
		try:
			markup.insert(InlineKeyboardButton(parcer_dagestan.cities[i], callback_data='dag_city_'+parcer_dagestan.cities[i]))
		except:
			if page != 1:
				last_page = True
				markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_dag_'+str(page)))
				break
	if page == 1 and last_page == False:
		markup.add(InlineKeyboardButton('Далее ⏩', callback_data='next_dag_'+str(page)))
	elif last_page == False:
		markup.insert(InlineKeyboardButton('⏪ Назад', callback_data='back_dag_'+str(page)))
		markup.insert(InlineKeyboardButton('Далее ⏩', callback_data='next_dag_'+str(page)))
	return markup

async def dag_city(address, period, user_id):
	markup = InlineKeyboardMarkup()
	zero_check = True
	if period == 'today':
		markup.insert(InlineKeyboardButton('На завтра', callback_data='dag_tomorrow')).insert(InlineKeyboardButton('На месяц', callback_data='dag_month'))
	else:
		markup.insert(InlineKeyboardButton('На сегодня', callback_data='dag_city_'+address)).insert(InlineKeyboardButton('На месяц', callback_data='dag_month'))
	for item in sqlite_bd.cur.execute(f'SELECT address FROM favorite_dagestan WHERE user_id == {user_id}').fetchall():
		if item[0] == address:
			zero_check = False
			markup.add(InlineKeyboardButton('Удалить из избранных', callback_data='dag_delete'))
			break
	if zero_check == True:
			markup.add(InlineKeyboardButton('Добавить в избранное', callback_data='dag_add'))
	return markup

async def dagestan_month():
	m = datetime.now().month
	y = datetime.now().year
	days = (date(y, m+1, 1) - date(y, m, 1)).days
	d1 = date(y, m, 1)
	d2 = date(y, m, days)
	d3 = d2 - d1
	days = [(d1 + timedelta(days=i)).strftime('%Y.%m.%d') for i in range(d3.days + 1)]

	count = 0
	markup = InlineKeyboardMarkup(row_width=5)
	for day in days:
		if count < 9:
			markup.insert(InlineKeyboardButton(day[9:], callback_data='dag_days_'+day[9:]))
		else:
			markup.insert(InlineKeyboardButton(day[8:], callback_data='dag_days_'+day[8:]))
		count += 1
	return markup

markup_tracker_menu = InlineKeyboardMarkup()
markup_tracker_menu.add(InlineKeyboardButton('Ввести самому', callback_data = 'tracker_myself')).add(InlineKeyboardButton('Рассчитать по датам', callback_data = 'tracker_calculate'))

async def markup_tracker(user_id):
	markup_tracker = InlineKeyboardMarkup(row_width=5)
	markup_tracker.add(InlineKeyboardButton('Намаз', callback_data='troth_salat')).insert(InlineKeyboardButton('Всего', callback_data='troth_current')).insert(InlineKeyboardButton('Нужно', callback_data='troth_need')).insert(InlineKeyboardButton('Минус', callback_data= 'calc_minus')).insert(InlineKeyboardButton('Плюс', callback_data='calc_add'))
	markup_tracker.add(InlineKeyboardButton('Фаджр', callback_data='troth_salat')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT fajr FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_current')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT fajr_need FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_need')).insert(InlineKeyboardButton('-', callback_data= 'minus_fajr')).insert(InlineKeyboardButton('+', callback_data='plus_fajr'))
	markup_tracker.add(InlineKeyboardButton('Зухр', callback_data='troth_salat')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT zuhr FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_current')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT zuhr_need FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_need')).insert(InlineKeyboardButton('-', callback_data='minus_zuhr')).insert(InlineKeyboardButton('+', callback_data='plus_zuhr'))
	markup_tracker.add(InlineKeyboardButton('Аср', callback_data='troth_salat')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT asr FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_current')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT asr_need FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_need')).insert(InlineKeyboardButton('-', callback_data='minus_asr')).insert(InlineKeyboardButton('+', callback_data='plus_asr'))
	markup_tracker.add(InlineKeyboardButton('Магриб', callback_data='troth_salat')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT magrib FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_current')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT magrib_need FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_need')).insert(InlineKeyboardButton('-', callback_data='minus_magrib')).insert(InlineKeyboardButton('+', callback_data='plus_magrib'))
	markup_tracker.add(InlineKeyboardButton('Иша', callback_data='troth_salat')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT isha FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_current')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT isha_need FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_need')).insert(InlineKeyboardButton('-', callback_data='minus_isha')).insert(InlineKeyboardButton('+', callback_data='plus_isha'))
	if sqlite_bd.cur.execute(f'SELECT vitr_need FROM tracker WHERE user_id == {user_id}').fetchone()[0] == '0':
		pass
	else:
		markup_tracker.add(InlineKeyboardButton('Витр', callback_data='tracker_salat')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT vitr FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='troth_current')).insert(InlineKeyboardButton(sqlite_bd.cur.execute(f'SELECT vitr_need FROM tracker WHERE user_id == {user_id}').fetchone()[0], callback_data='tracker_need')).insert(InlineKeyboardButton('-', callback_data='minus_vitr')).insert(InlineKeyboardButton('+', callback_data='plus_vitr'))
	return markup_tracker

markup_tracker_reset = InlineKeyboardMarkup()
markup_tracker_reset.add(InlineKeyboardButton('Отмена', callback_data='tracker_cancel')).insert(InlineKeyboardButton('Сбросить', callback_data = 'tracker_reset'))

markup_tracker_vitr = InlineKeyboardMarkup()
markup_tracker_vitr.add(InlineKeyboardButton('Нет', callback_data='vitr_no')).insert(InlineKeyboardButton('Да', callback_data='vitr_yes'))

markup_dua = InlineKeyboardMarkup(row_width=2)
markup_dua.add(InlineKeyboardButton('Адама (мир Ему)', callback_data='dua_1')).add(InlineKeyboardButton('Айюба (мир Ему)', callback_data='dua_2')).insert(InlineKeyboardButton('Мусы (мир Ему) (1)', callback_data='dua_8')).insert(InlineKeyboardButton('Ибрахима (мир Ему) (1)', callback_data='dua_3')).insert(InlineKeyboardButton('Мусы (мир Ему) (2)', callback_data='dua_9')).insert(InlineKeyboardButton('Ибрахима (мир Ему) (2)', callback_data='dua_4')).insert(InlineKeyboardButton('Шуайба (мир Ему)', callback_data='dua_10')).insert(InlineKeyboardButton('Ибрахима (мир Ему) (3)', callback_data='dua_5')).insert(InlineKeyboardButton('Йусуфа (мир Ему)', callback_data='dua_11')).insert(InlineKeyboardButton('Ибрахима (мир Ему) (4)', callback_data='dua_6')).insert(InlineKeyboardButton('Йунуса (мир Ему)', callback_data='dua_12')).insert(InlineKeyboardButton('Ибрахима (мир Ему) (5)', callback_data='dua_7')).insert(InlineKeyboardButton('Лута (мир Ему)', callback_data='dua_13'))

markup_dua_lower = InlineKeyboardMarkup()
markup_dua_lower.add(InlineKeyboardButton('Список дуа', callback_data='dua_all'))

markup_hadis = InlineKeyboardMarkup()
markup_hadis.add(InlineKeyboardButton('Сохраненные хадисы', callback_data='hadis_favorite')).insert(InlineKeyboardButton('Случайный хадис', callback_data='hadis_random'))

async def markup_hadis_random(count, user_id):
	markup = InlineKeyboardMarkup()
	info = sqlite_bd.cur.execute(f'SELECT EXISTS(SELECT hadis_id FROM hadis WHERE user_id == ? AND hadis_id == ?)', (user_id, count))
	if info.fetchone()[0] == 0:
		markup.add(InlineKeyboardButton('Сохранить', callback_data='hadis_favorite_add_'+str(count)))
	else:
		markup.add(InlineKeyboardButton('Удалить из сохраненных', callback_data='hadis_favorite_delete_'+str(count)))
	markup.insert(InlineKeyboardButton('Ещё', callback_data='hadis_random'))
	return markup

async def hadis_favorite(user_id, page):
	markup = InlineKeyboardMarkup()
	last_page = False
	keys = page * 5
	for i in range(keys-5, keys):
		try:
			key = sqlite_bd.cur.execute('SELECT hadis_id FROM hadis WHERE user_id == ? AND id == ?', (user_id, i + 1)).fetchone()[0]
			text = await parcer_hadis.get_hadis(int(key))
			markup.add(InlineKeyboardButton(text, callback_data='hadis_saved_' + key))
			key_check = sqlite_bd.cur.execute('SELECT hadis_id FROM hadis WHERE user_id == ? AND id == ?', (user_id, i + 2)).fetchone()[0]
		except:
			last_page = True
			if page != 1:
				markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_hadis_'+str(page)))
				break
	if page == 1 and last_page == False:
		markup.add(InlineKeyboardButton('Далее ⏩', callback_data='next_hadis_'+str(page)))
	elif last_page == False:
		markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_hadis_'+str(page)))
		markup.insert(InlineKeyboardButton('Далее ⏩', callback_data='next_hadis_'+str(page)))
	return markup

async def names_inline(page):
	markup = InlineKeyboardMarkup(row_width=5)
	key = 25 * page
	last_page = False
	for i in range(key - 25, key):
		markup.insert(InlineKeyboardButton(i + 1, callback_data='names_'+str(i + 1)))
		if i == 98:
			last_page = True
			markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_names_'+str(page)))
			return markup
	if page == 1 and last_page == False:
		markup.add(InlineKeyboardButton('Далее ⏩', callback_data='next_names_'+str(page)))
	elif last_page == False:
		markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_names_'+str(page)))
		markup.insert(InlineKeyboardButton('Далее ⏩', callback_data='next_names_'+str(page)))
	return markup

async def names_photo_inline(count):
	markup = InlineKeyboardMarkup()
	if count == 1:
		markup.add(InlineKeyboardButton('Все имена', callback_data = 'all_names')).insert(InlineKeyboardButton('Далее ⏩', callback_data='next_photo_'+str(count)))
	elif count == 99:
		markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_photo_'+str(count))).insert(InlineKeyboardButton('Все имена', callback_data = 'all_names'))
	else:
		markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_photo_'+str(count))).insert(InlineKeyboardButton('Все имена', callback_data = 'all_names')).insert(InlineKeyboardButton('Далее ⏩', callback_data='next_photo_'+str(count)))
	return markup

async def food_markup(page):
	markup = InlineKeyboardMarkup()
	if page == 1:
		markup.add(InlineKeyboardButton('Далее ⏩', callback_data='next_food_'+str(page)))
	elif page == 10:
		markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_food_'+str(page)))
	else:
		markup.add(InlineKeyboardButton('⏪ Назад', callback_data='back_food_'+str(page))).insert(InlineKeyboardButton('Далее ⏩', callback_data='next_food_'+str(page)))
	return markup