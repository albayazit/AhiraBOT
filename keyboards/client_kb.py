import re
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from parcer import parcer_exel
from datetime import date, timedelta, datetime


# кнопки
button_time = KeyboardButton('🕦 Время намаза')

button_tutor = KeyboardButton('🕌 Обучение')
button_tutor_what = KeyboardButton('❓\n Что такое намаз')
button_tutor_time = KeyboardButton('🕦\n Время намазов')
button_tutor_cond = KeyboardButton('❗\n Условия намаза')
button_tutor_gusl = KeyboardButton('🚿\n Гусль')
button_tutor_taharat = KeyboardButton('💧\n Тахарат')
button_tutor_forma = KeyboardButton('🧎\n Форма совершения намаза')
button_tutor_sura = KeyboardButton('📃\n Суры и дуа намаза')
button_tutor_women = KeyboardButton('🧕\n Женский намаз')
 
button_audio = KeyboardButton('🎧 Аудио')
button_audio_koran = KeyboardButton('📕\n Коран')
button_audio_hutba = KeyboardButton('📢\n Проповедь')

button_books = KeyboardButton('📚 Книги')
button_hadis = KeyboardButton('📖 Хадисы')
button_dua = KeyboardButton('🤲 Дуа')
button_zikr = KeyboardButton('📿 Зикр')
button_tracker = KeyboardButton('📈 Трекер')
button_info = KeyboardButton('❗ Помощь')
button_calendar = KeyboardButton('📅 Календарь')
button_back = KeyboardButton('⏪ Назад')


back_tat = InlineKeyboardButton('⏪ Назад', callback_data='back_tat')
next_tat = InlineKeyboardButton('Далее ⏩', callback_data='next_tat')

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

# клавиатура главного экрана
markup_main = ReplyKeyboardMarkup()
markup_main.add(button_time).add(
    button_tracker, button_audio, button_books, button_hadis, button_dua, button_zikr, button_tutor, button_info, button_calendar
)


# клавиатура обучения
markup_namaz_tutor = ReplyKeyboardMarkup()
markup_namaz_tutor.add(
    button_tutor_what, button_tutor_time, button_tutor_cond, button_tutor_gusl, button_tutor_taharat, button_tutor_forma, button_tutor_sura, button_tutor_women, button_back
)

# клавиатура аудио
markup_audio = ReplyKeyboardMarkup()
markup_audio.add(
    button_audio_koran, button_audio_hutba
).add(button_back)


# выбор региона
inline_favorite = InlineKeyboardMarkup()
inline_favorite.add(InlineKeyboardButton('Добавить город', callback_data='add_city'))

inline_namaz_time = InlineKeyboardMarkup()
inline_namaz_time.add(InlineKeyboardButton('Татарстан', callback_data='tatarstan')).add(InlineKeyboardButton('Другой регион', callback_data='other_region'))


#--- При выборе Татарстана ---#
def inline_namaz_time_tat(page):
	last_page = False
	markup = InlineKeyboardMarkup(row_width=2)
	keys = page*10
	for i in range(keys-10, keys):
		try:
			markup.insert(InlineKeyboardButton(parcer_exel.cities_exel[i], callback_data=parcer_exel.cities_exel[i]))
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


# инлайн города

def inline_city(period, current_city):
    inline_city = InlineKeyboardMarkup(row_width=3)
    if period == 'today':
        inline_city.insert(InlineKeyboardButton('На завтра', callback_data = 'tomorrow_time')).insert(InlineKeyboardButton('На месяц', callback_data='month_time'))
    elif period == 'tomorrow':
        inline_city.insert(InlineKeyboardButton('На сегодня', callback_data=current_city)).insert(InlineKeyboardButton('На месяц', callback_data='month_time'))
    return inline_city

# инлайн зикра
inline_zikr_all = InlineKeyboardMarkup()
inline_zikr_all.row_width = 2
inline_zikr_all.add(zikr_1, zikr_2, zikr_3, zikr_4, zikr_5, zikr_6, zikr_7, zikr_8, zikr_9, zikr_10, zikr_11, zikr_12, zikr_13, zikr_14, zikr_15, zikr_16, zikr_17)

inline_zikr_1 = InlineKeyboardMarkup().add(InlineKeyboardButton('+', callback_data='+_1'))


# Все дни месяца
def month_days():
	m = datetime.now().month
	y = datetime.now().year
	days = (date(y, m+1, 1) - date(y, m, 1)).days
	d1 = date(y, m, 1)
	d2 = date(y, m, days)
	d3 = d2 - d1
	return [(d1 + timedelta(days=i)).strftime('%Y.%m.%d') for i in range(d3.days + 1)]


def inline_month():
	count = 0
	markup = InlineKeyboardMarkup(row_width=3)
	days = month_days()
	for day in days:
		if count < 9:
			markup.insert(InlineKeyboardButton(day[9:], callback_data='tatarstan'+day))
		else:
			markup.insert(InlineKeyboardButton(day[8:], callback_data='tatarstan'+day))
		count += 1
	return markup