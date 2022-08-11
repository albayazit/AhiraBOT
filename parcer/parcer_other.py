import requests
from database import sqlite_bd
from datetime import datetime

# methods
methods = {
	'1':'MWL Всемирная лига мусульман',
	'2':'Islamic Society of North America',
	'3':'Egyptian General Authority of Survey',
	'4':'Umm Al-Qura University, Makkah',
	'5':'University of Islamic Sciences, Karachi',
	'6':'University of Tehran',
	'7':'Shia Ithna-Ashari',
	'8':'Gulf Region',
	'9':'Kuwait',
	'10':'Qatar',
	'11':'Majlis Ugama Islam Singapura, Singapore',
	'12':'Union Organization islamic de France',
	'13':'Diyanet, Turkey',
	'14':'ДУМ России'
}
# calculate schools
schools = {
	'0':'Стандартный',
	'1':'Ханафитский'
}
schools_from_json = {
	'STANDARD':'Стандартный',
	'HANAFI':'Ханафитский'
}

# check city in bd
async def city_check(address):
	url = "https://aladhan.p.rapidapi.com/timingsByAddress"
	querystring = {"address":str(address)}
	headers = {
		"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
		"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring).json()
	return response['data']['timings']

# get time for day
async def get_day_time(state):
	async with state.proxy() as data:
		result = tuple(data.values())
	url = "https://aladhan.p.rapidapi.com/timingsByAddress"
	querystring = {"address":result[0],"school":result[1]}
	headers = {
		"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
		"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
	}
	try:
		response = requests.request("GET", url, headers=headers, params=querystring).json()
		times = response['data']['timings']
		date = response['data']['date']
		meta = response['data']['meta']['method']['id']
		daytime_message = (
					f'🌍 Город: <b>{result[0]}</b>\n\n'
					f'📅 Дата: <b>{date["gregorian"]["date"].replace("-", ".")} | {date["hijri"]["date"].replace("-", ".")}</b>\n\n'
					f'🔭 Метод расчета: <b> {methods[str(meta)]} | {schools[result[1]]}</b>\n\n'

					f'<b>Фаджр - {times["Fajr"]}</b>\n'
					f'<b>Зухр - {times["Dhuhr"]}</b>\n'
					f'<b>Аср - {times["Asr"]}</b>\n'
					f'<b>Магриб - {times["Maghrib"]}</b>\n'
					f'<b>Иша - {times["Isha"]}</b>\n\n'
					
					f'Рассвет: <b>{times["Sunrise"]}</b>\n'
					f'Середина ночи: <b>{times["Midnight"]}</b>\n'
					f'Последняя 1/3 ночи: <b>{times["Lastthird"]}</b>'
			)
		return daytime_message
	except:
		print('Parcing ERROR')

# get time for day in favorite_cities
async def get_day_time_from_menu(user_id, address):
	school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address)).fetchone()
	url = "https://aladhan.p.rapidapi.com/timingsByAddress"
	querystring = {"address":address,"school":school[0]}
	headers = {
		"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
		"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring).json()
	times = response['data']['timings']
	date = response['data']['date']
	meta = response['data']['meta']['method']['id']

	daytime_message = (
				f'🌍 Город: <b>{address}</b>\n\n'
				f'📅 Дата: <b>{date["gregorian"]["date"].replace("-", ".")} | {date["hijri"]["date"].replace("-", ".")}</b>\n\n'
				f'🔭 Метод расчета: <b> {methods[str(meta)]} | {schools[school[0]]}</b>\n\n'

				f'<b>Фаджр - {times["Fajr"]}</b>\n'
				f'<b>Зухр - {times["Dhuhr"]}</b>\n'
				f'<b>Аср - {times["Asr"]}</b>\n'
				f'<b>Магриб - {times["Maghrib"]}</b>\n'
				f'<b>Иша - {times["Isha"]}</b>\n\n'
				
				f'Рассвет: <b>{times["Sunrise"]}</b>\n'
				f'Середина ночи: <b>{times["Midnight"]}</b>\n'
				f'Последняя 1/3 ночи: <b>{times["Lastthird"]}</b>'
		)
	return daytime_message


async def get_calendar_time(address, day, school):
	month = datetime.now().month
	year = datetime.now().year

	url = "https://aladhan.p.rapidapi.com/calendarByAddress"

	querystring = {"address":address,"year":year,"month":month, "school":school}

	headers = {
		"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
		"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring).json()
	current_day = int(day) - 1
	try:
		data = response['data'][current_day]
	except:
		get_function = await get_for_next_month(address, school)
		data = get_function['data'][0]
	date = data['date']
	meta = data['meta']['method']['id']
	times = data['timings']
	school = data['meta']['school']

	message = (
				f'🌍 Город: <b>{address}</b>\n\n'
				f'📅 Дата: <b>{date["gregorian"]["date"].replace("-", ".")} | {date["hijri"]["date"].replace("-", ".")}</b>\n\n'
				f'🔭 Метод расчета: <b> {methods[str(meta)]} | {schools_from_json[school]}</b>\n\n'

				f'<b>Фаджр - {times["Fajr"][:5]}</b>\n'
				f'<b>Зухр - {times["Dhuhr"][:5]}</b>\n'
				f'<b>Аср - {times["Asr"][:5]}</b>\n'
				f'<b>Магриб - {times["Maghrib"][:5]}</b>\n'
				f'<b>Иша - {times["Isha"][:5]}</b>\n\n'
				
				f'Рассвет: <b>{times["Sunrise"][:5]}</b>\n'
				f'Середина ночи: <b>{times["Midnight"][:5]}</b>\n'
				f'Последняя 1/3 ночи: <b>{times["Lastthird"][:5]}</b>'
		)
	return message


async def get_for_next_month(address, school):
	month = datetime.now().month
	year = datetime.now().year
	headers = {
		"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
		"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
	}
	url = "https://aladhan.p.rapidapi.com/calendarByAddress"
	if month == '12':
		querystring = {"address":address,"year":year + 1,"month":'1', "school":school}
		response = requests.request("GET", url, headers=headers, params=querystring).json()
	else:
		querystring = {"address":address,"year":year,"month":month + 1, "school":school}
		response = requests.request("GET", url, headers=headers, params=querystring).json()
	return response