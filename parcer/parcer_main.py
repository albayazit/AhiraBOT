import requests
from database import sqlite_bd

# calculate methods
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
	querystring = {"address":result[0],"method":result[1],"school":result[2]}
	headers = {
		"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
		"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
	}
	try:
		response = requests.request("GET", url, headers=headers, params=querystring).json()
		times = response['data']['timings']
		date = response['data']['date']

		daytime_message = (
					f'🌍 Город: <b>{result[0]}</b>\n\n'
					f'📅 Дата: <b>{date["gregorian"]["date"].replace("-", ".")} | {date["hijri"]["date"].replace("-", ".")}</b>\n\n'
					f'🔭 Метод расчета: <b>{methods[result[1]]} | {schools[result[2]]}</b>\n\n'

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
		return "Ой, что-то пошло не так, повторите попытку!"

# get time for day in favorite_cities
async def get_day_time_from_menu(user_id, address):
	method = sqlite_bd.cur.execute('SELECT method FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address)).fetchone()
	school = sqlite_bd.cur.execute('SELECT school FROM favorite_other WHERE user_id == ? AND address = ?', (user_id, address)).fetchone()
	url = "https://aladhan.p.rapidapi.com/timingsByAddress"
	querystring = {"address":address,"method":method[0],"school":school[0]}
	headers = {
		"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
		"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring).json()
	times = response['data']['timings']
	date = response['data']['date']

	daytime_message = (
				f'🌍 Город: <b>{address}</b>\n\n'
				f'📅 Дата: <b>{date["gregorian"]["date"].replace("-", ".")} | {date["hijri"]["date"].replace("-", ".")}</b>\n\n'
				f'🔭 Метод расчета: <b>{methods[method[0]]} | {schools[school[0]]}</b>\n\n'

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