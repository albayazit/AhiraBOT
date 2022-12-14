import requests
import datetime as dt
from datetime import date, datetime

links = {
	'Махачкала':'mahashkala.json',
	'Агул':'agul.json',
	'Ахты':'ahti.json',
	'Ахвах':'ahvah.json',
	'Бабаюрт':'babayurt.json',
	'Ботлих':'botlih.json',
	'Буйнакск':'buynaksk.json',
	'Цумада':'cumada.json',
	'Даг-Огни':'dagogni.json',
	'Дербент':'derbent.json',
	'Гергебиль':'gergebil.json',
	'Гумбет':'gumbet.json',
	'Хасавюрт':'hasavyurt.json',
	'Хунзах':'hunzah.json',
	'Избербаш':'izberbash.json',
	'Каспийск':'kaspiysk.json',
	'Дылым':'kazbek.json',
	'Кизилюрт':'kizilurt.json',
	'Кизляр':'kizlyar.json',
	'Курах':'kurah.json',
	'Леваши':'levashi.json',
	'Рутул':'rutul.json',
	'Шамилькала':'shamilkala.json',
	'Чарода':'sharoda.json',
	'Южно-Сухокумск':'suhokumsk.json',
	'Тлярата':'tlarata.json',
	'Унцукуль':'unsukul.json'
}

cities = list(links.keys())
headers = {
	'cookie':'beget=begetok',
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42'
	}

async def get_day_time(address):
	year = datetime.today().year
	day = datetime.today().strftime('%j')
	today = datetime.today().day
	url = f"https://muftiyatrd.ru/json/namaz/{links[address]}"
	response = requests.request("GET", url, headers=headers).json()
	data = response[int(day)-1]
	daytime_message = (
		f'🌍 Город: <b>{address}</b>\n\n'
		f'📅 Дата: <b>{date.today().strftime("%d.%m.%Y")}</b>\n\n'
		f'🔭 Метод расчета: <b>Муфтият Дагестана</b>\n\n'

		f'<b>Фаджр - {data["namaz_1"]}</b>\n'
		f'<b>Зухр - {data["namaz_2"]}</b>\n'
		f'<b>Аср - {data["namaz_3"]}</b>\n'
		f'<b>Магриб - {data["namaz_4"]}</b>\n'
		f'<b>Иша - {data["namaz_5"]}</b>\n\n'
		
		f'Рассвет: <b>{data["voshod"]}</b>\n'
	)
	return daytime_message

async def get_tomorrow_time(address):
	year = datetime.today().year
	day = datetime.today().strftime('%j')
	today = datetime.today().day
	url = f"https://muftiyatrd.ru/json/namaz/{links[address]}"
	response = requests.request("GET", url, headers=headers).json()
	try:
		data = response[int(day)]
	except:
		return 'Время на данный период еще недоступен!'
	tomorrow_message = (
		f'🌍 Город: <b>{address}</b>\n\n'
		f'📅 Дата: <b>{(date.today() + dt.timedelta(days=1)).strftime("%d.%m.%Y")}</b>\n\n'
		f'🔭 Метод расчета: <b>Муфтият Дагестана</b>\n\n'

		f'<b>Фаджр - {data["namaz_1"]}</b>\n'
		f'<b>Зухр - {data["namaz_2"]}</b>\n'
		f'<b>Аср - {data["namaz_3"]}</b>\n'
		f'<b>Магриб - {data["namaz_4"]}</b>\n'
		f'<b>Иша - {data["namaz_5"]}</b>\n\n'
		
		f'Рассвет: <b>{data["voshod"]}</b>\n'
	)
	return tomorrow_message

async def get_month_time(address, period):
	year = datetime.today().year
	day = datetime.today().strftime('%j')
	today = datetime.today().day
	current = int(day) - int(today)
	current_day = current + int(period) - 1
	url = f"https://muftiyatrd.ru/json/namaz/{links[address]}"
	response = requests.request("GET", url, headers=headers).json()
	data = response[current_day]
	today_full = datetime.today()
	current = today_full - dt.timedelta(days=today) + dt.timedelta(days=int(period))
	month_message = (
		f'🌍 Город: <b>{address}</b>\n\n'
		f'📅 Дата: <b>{current.strftime("%d.%m.%Y")}</b>\n\n'
		f'🔭 Метод расчета: <b>Муфтият Дагестана</b>\n\n'

		f'<b>Фаджр - {data["namaz_1"]}</b>\n'
		f'<b>Зухр - {data["namaz_2"]}</b>\n'
		f'<b>Аср - {data["namaz_3"]}</b>\n'
		f'<b>Магриб - {data["namaz_4"]}</b>\n'
		f'<b>Иша - {data["namaz_5"]}</b>\n\n'
		
		f'Рассвет: <b>{data["voshod"]}</b>\n'
	)
	return month_message