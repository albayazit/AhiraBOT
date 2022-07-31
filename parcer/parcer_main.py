import requests

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
schools = {
	'0':'Стандартный',
	'1':'Ханафитский'
}

# get for day
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
					f'📅 Дата: <b>{date["gregorian"]["date"].replace("-", ".")} | {date["hijri"]["date"].replace("-", ".")}</b>\n'
					f'Месяц: {date["hijri"]["month"]["ar"]}\n\n'
					f'🔭 Метод расчета: <b>{methods[result[1]]} | {schools[result[2]]}</b>\n\n'

					f'<b>Фаджр - {times["Fajr"]}</b>\n'
					f'<b>Зухр - {times["Dhuhr"]}</b>\n'
					f'<b>Аср - {times["Asr"]}</b>\n'
					f'<b>Магриб - {times["Maghrib"]}</b>\n'
					f'<b>Иша - {times["Isha"]}</b>\n\n'
					
					f'Рассвет: <b>{times["Sunrise"]}</b>\n'
					f'Первая 1/3 ночи: <b>{times["Firstthird"]}</b>\n'
					f'Середина ночи: <b>{times["Midnight"]}</b>\n'
					f'Последняя 1/3 ночи: <b>{times["Lastthird"]}</b>'
			)
		return daytime_message
	except:
		return "Ой, такого города не нашлось, проверьте название!"



# get for month

# url = "https://aladhan.p.rapidapi.com/calendarByAddress"

# querystring = {"address":"Казань","method":"2","school":"1"}

# headers = {
# 	"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
# 	"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers, params=querystring).json()

# print(response['data'][0]['timings']['Fajr'])