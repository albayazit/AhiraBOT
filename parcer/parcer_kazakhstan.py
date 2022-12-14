import requests
from datetime import datetime

cities_data = {
	'Нұр-Сұлтан': '51.133333/71.433333', 
	'Алматы': '43.238293/76.945465', 
	'Шымкент': '42.3/69.6', 
	'Арал': '46.8/61.666667', 
	'Байқоныр': '45.966111/63.307778', 
	'Жітіқара ауданы ': '51.937054/61.012478', 
	'Ұзынкөл ауданы ': '54.162521/65.474446', 
	'Денис ауданы': '52.603040/61.620629', 
	'Лисаков': '52.544079/62.492641', 
	'Жәнібек': '49.416667/46.85', 
	'Жаркент': '44.166667/80.00', 
	'Қызылорда': '44.85/65.516667', 
	'Ақсай': '51.10/52.59', 
	'Чапаев': '50.182778/51.175278', 
	'Жаңқала': '49.215139/50.303028', 
	'Бейнеу': '45.322946/55.188862', 
	'Ақтөбе': '50.3/57.166667', 
	'Қандыағаш': '49.474444/57.423333', 
	'Хромтау': '50.250278/58.434722', 
	'Шалқар': '47.831392/59.619290', 
	'Қапшағай': '43.883333/77.083333', 
	'Талдықорған': '45.016667/78.366667', 
	'Таран ауданы': '52.539620/62.771083', 
	'Амангелді ауданы': '49.940951/65.461268', 
	'Федеров ауданы': '53.692845/62.851689', 
	'Жангелді ауданы': '49.699308/63.631067', 
	'Қарасу ауданы': '52.341344/65.392026', 
	'Меңдіқара ауданы': '53.933550/64.299378', 
	'Науырзым  ауданы ': '51.304292/63.628399',
	'Сарыкөл ауданы': '53.440801/65.685604',
	'Әулиекөл ауданы': '52.224572/63.920163',
	'Көкшетау': '53.291667/69.391667', 
	'Сарыөзек': '44.356667/77.969167', 
	'Степногорск': '52.346944/71.881667', 
	'Үшарал': '46.169722/80.939444', 
	'Атбасар': '51.816667/68.35', 
	'Аягөз': '47.966667/80.433333', 
	'Өскемен': '49.95/82.616667', 
	'Риддер': '50.35/83.516667', 
	'Семей': '50.411111/80.2275', 
	'Жаңатас': '43.566667/69.75', 
	'Қаратау': '43.166667/70.466667', 
	'Тараз': '42.883333/71.366667', 
	'Балқаш': '46.5408/74.8789', 
	'Жәйрем': '48.3375/70.169167', 
	'Жезқазған': '47.783333/67.7', 
	'Сәтпаев': '47.9/67.533333', 
	'Қарағанды': '49.806406/73.085485', 
	'Арқалық': '50.248611/66.911389', 
	'Қостанай': '53.219333/63.634194', 
	'Рудный': '52.966667/63.116667', 
	'Петропавл': '54.862222/69.140833', 
	'Екібастұз': '51.729778/75.326583', 
	'Павлодар': '52.315556/76.956389', 
	'Әйтеке би кенті': '45.835934/62.148317', 
	'Жетісай': '40.775278/68.327222', 
	'Сарыағаш': '41.466667/69.166667', 
	'Шардара': '41.254722/67.969167', 
	'Миялы': '48.47/53.47', 
	'Атырау': '47.116667/51.883333',
	'Мақат': '47.65/53.316667',
	'Құлсары': '46.983333/54.016667',
	'Ақтау': '43.635379/51.169135',
	'Жаңаөзен': '43.343266/52.865792',
	'Форт-Шевченко': '44.507463/50.262833',
	'Сайқын': '48.815278/46.766944', 
	'Орал': '51.204019/51.370537', 
	'Түркістан': '43.3/68.243611', 
	'Қарабалық ауданы': '53.599507/61.769785', 
	'Қамысты ауданы': '51.549566/62.301561', 
	'Алтынсарин ауданы': '53.104086/64.589965', 
	'Ұзынағаш': '43.220905/76.314192', 
	'Талғар': '43.302813/77.239690', 
	'Қаскелең': '43.202449/76.622278', 
	'Шұбарқұдық': '49.202977/56.563994', 
	'Шу': '43.611782/73.760237', 
	'Қордай': '43.046040/74.708076', 
	'Қаражал': '48.001042/70.785762', 
	'Атасу ауылы': '48.500979/71.078065', 
	'Келес ауданы': '41.305597/68.544861', 
	'Ленгер': '42.182051/69.882120', 
	'Отырар ауданы': '42.666225/67.497308', 
	'Сайрам ауданы': '42.403930/69.875266', 
	'Созақ ауданы': '44.861720/68.569600', 
	'Түлкібас кенті': '42.493477/70.290737', 
	'Қарғалы': '50.783970/58.106976', 
	'Ойыл ауданы': '49.260606/54.575097', 
	'Ырғыз ауданы': '48.481065/62.151353', 
	'Байғанин ауданы': '47.436554/56.526355', 
	'Қобда ауданы': '50.188476/55.325909',
	'Мәртөк ауданы': '50.711441/56.733892',
	'Ембі': '48.823344/58.148397', 
	'Шиелі кенті': '44.177802/66.731387', 
	'Зайсан': '47.453008/84.969846', 
	'Шал ақын ауданы': '53.785566/67.379494', 
	'Еңбекшіқазақ': '43.500438/78.163706', 
	'Индер': '48.299901/51.398492', 
	'Жосалы': '45.488489/64.086666', 
	'Кентау': '43.518131/68.504652', 
	'Қазығұрт': '41.862652/69.579316', 
	'Шамалған ауылы': '43.189863/76.534549', 
	'Тайынша': '53.852738/69.782631', 
	'Жезді кенті': '48.058857/67.054870', 
	'Сырым ауданы': '50.325986/52.678107', 
	'Жалағаш кенті': '45.080281/64.681333', 
	'Тереңөзек кенті': '45.053372/64.985412', 
	'Жаңақорған кенті': '43.900451/67.243723', 
	'Теміртау': '50.058756/72.953424', 
	'Алға': '50.076944/58.284444', 
	'Ақсу': '52.037890/76.920582', 
	'Май ауданы': '51.030109/77.498594', 
	'Шарбақты ауданы': '52.335401/78.302622', 
	'Ертіс ауданы': '53.295153/74.586606', 
	'Ақтоғай ауданы': '52.732339/75.222892', 
	'Тереңкөл ауданы': '53.227323/76.483156', 
	'Баянауыл ауданы': '50.803357/75.489287', 
	'Аққулы ауданы': '51.508573/78.303592', 
	'Солнечный': '52.034976/75.462284', 
	'Майқайын кенті': '51.458711/75.796313', 
	'Шаян': '43.032169/69.381210',
	'Әйтеке би ауданы': '49.99/60.87',
	'Целиноград ауданы': '51.028562/70.990677', 
	'Ұржар ауданы': '46.974805/81.462482', 
	'Көкпекті ауданы': '48.687009/82.892842', 
	'Курчатов': '50.754900/78.544826', 
	'Исатай ауданы': '47.381847/50.381465', 
	'Құрманғазы ауданы': '47.140203/49.266377', 
	'Маханбет ауданы': '47.633313/51.763577', 
	'Жосалы кенті': '45.488495/64.086675', 
	'Бәйдібек ауданы': '43.027233/69.485514', 
	'Арыс қаласы': '42.432744/68.813798', 
	'Мырзакент кенті': '40.666728/68.544933', 
	'Теңіз кен орны': '46.079223/53.387326', 
	'Қосшы': '50.970262/71.355366', 
	'Ойыл ауданы': '49.260612/54.575097'
	}
cities = list(cities_data.keys())

async def get_day_time(address):
	year = datetime.today().year
	day = datetime.today().strftime('%j')
	today = datetime.today().day
	url = f"https://api.muftyat.kz/prayer-times/{year}/{cities_data[address]}?format=json"
	response = requests.request("GET", url).json()
	data = response['result'][int(day)-1]
	date = datetime.fromisoformat(data['Date'])
	daytime_message = (
				f'🌍 Город: <b>{address}</b>\n\n'
				f'📅 Дата: <b>{date.strftime("%d.%m.%Y")}</b>\n\n'
				f'🔭 Метод расчета: <b> ДУМ Казахстана</b>\n\n'

				f'<b>Фаджр - {data["fajr"]}</b>\n'
				f'<b>Зухр - {data["dhuhr"]}</b>\n'
				f'<b>Аср - {data["asr"]}</b>\n'
				f'<b>Магриб - {data["maghrib"]}</b>\n'
				f'<b>Иша - {data["isha"]}</b>\n\n'
				
				f'Рассвет: <b>{data["sunrise"]}</b>\n'
				f'Середина ночи: <b>{data["midnight"]}</b>\n'
		)
	return daytime_message

async def get_tomorrow_time(address):
	year = datetime.today().year
	day = datetime.today().strftime('%j')
	today = datetime.today().day
	url = f"https://api.muftyat.kz/prayer-times/{year}/{cities_data[address]}?format=json"
	next_year = int(year) + 1
	response = requests.request("GET", url).json()
	try:
		data = response['result'][int(day)]
	except:
		url = f"https://api.muftyat.kz/prayer-times/{next_year}/{cities_data[address]}?format=json"
		response = requests.request("GET", url).json()
		data = response['result'][0]
	date = datetime.fromisoformat(data['Date'])
	daytime_message = (
				f'🌍 Город: <b>{address}</b>\n\n'
				f'📅 Дата: <b>{date.strftime("%d.%m.%Y")}</b>\n\n'
				f'🔭 Метод расчета: <b> ДУМ Казахстана</b>\n\n'

				f'<b>Фаджр - {data["fajr"]}</b>\n'
				f'<b>Зухр - {data["dhuhr"]}</b>\n'
				f'<b>Аср - {data["asr"]}</b>\n'
				f'<b>Магриб - {data["maghrib"]}</b>\n'
				f'<b>Иша - {data["isha"]}</b>\n\n'
				
				f'Рассвет: <b>{data["sunrise"]}</b>\n'
				f'Середина ночи: <b>{data["midnight"]}</b>\n'
		)
	return daytime_message

async def get_month_time(address, period):
	year = datetime.today().year
	day = datetime.today().strftime('%j')
	today = datetime.today().day
	current = int(day) - int(today)
	current_day = current + int(period) - 1
	url = f"https://api.muftyat.kz/prayer-times/{year}/{cities_data[address]}?format=json"	
	response = requests.request("GET", url).json()
	data = response['result'][current_day]
	date = datetime.fromisoformat(data['Date'])
	daytime_message = (
				f'🌍 Город: <b>{address}</b>\n\n'
				f'📅 Дата: <b>{date.strftime("%d.%m.%Y")}</b>\n\n'
				f'🔭 Метод расчета: <b> ДУМ Казахстана</b>\n\n'

				f'<b>Фаджр - {data["fajr"]}</b>\n'
				f'<b>Зухр - {data["dhuhr"]}</b>\n'
				f'<b>Аср - {data["asr"]}</b>\n'
				f'<b>Магриб - {data["maghrib"]}</b>\n'
				f'<b>Иша - {data["isha"]}</b>\n\n'
				
				f'Рассвет: <b>{data["sunrise"]}</b>\n'
				f'Середина ночи: <b>{data["midnight"]}</b>\n'
		)
	return daytime_message