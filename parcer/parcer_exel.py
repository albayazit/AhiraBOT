# парсим время намаза для Татарстана с exel
from datetime import datetime, timedelta
import calendar
import pandas as pd
import datetime

from parcer import parcer_hidjra

cl = calendar.Calendar()
tat_table = pd.read_excel('data/namaz/namaz_time_tatarstan.xlsx')
tat_table['day'] = tat_table['day'].dt.strftime('%Y.%m.%d') # преобразуем 'day' в строку
current_date = datetime.date.today() # получаем сегодняшнюю дату
nextday_date = current_date + datetime.timedelta(days=1)
cities_exel = tat_table['city'].unique()

def get_day_time(current_city):
    time_day = tat_table[(tat_table['city'] == current_city) & (tat_table['day'] == current_date.strftime('%Y.%m.%d'))]
    isha_time_th = current_date.strftime('%d.%m.%Y') + ' ' + time_day["isha"].to_string()[-8:]
    fajr_time_th = nextday_date.strftime('%d.%m.%Y') + ' ' + time_day["fajr"].to_string()[-8:]

    isha_time_dt = datetime.datetime.strptime(isha_time_th, '%d.%m.%Y %H:%M:%S')
    fajr_time_dt = datetime.datetime.strptime(fajr_time_th, '%d.%m.%Y %H:%M:%S')

    difference = (isha_time_dt - fajr_time_dt).total_seconds()
    current_sec = fajr_time_dt - timedelta(seconds=difference/-3)
    tahadjud_time = datetime.datetime.strftime(current_sec, '%H:%M')

    daytime_message = (
        f'🌍 Город: <b>{current_city}</b>\n\n'
        f'📅 Дата: <b>{current_date.strftime("%d.%m.%Y")} | {parcer_hidjra.main()}</b>\n\n'
        '🔭 Метод расчета: <b>ДУМ РТ</b>\n\n'
        f'Фаджр - <b>{time_day["fajr"].to_string()[-8:-3]}</b>\n'
        f'Фаджр в мечети - <b>{time_day["fajr_mosque"].to_string()[-8:-3]}</b>\n'
        f'Зухр - <b>{time_day["zuhr"].to_string()[-8:-3]}</b>\n'
        f'Аср - <b>{time_day["asr"].to_string()[-8:-3]}</b>\n'
        f'Магриб - <b>{time_day["magrib"].to_string()[-8:-3]}</b>\n'
        f'Иша - <b>{time_day["isha"].to_string()[-8:-3]}</b>\n\n'
        
        f'Рассвет: <b>{time_day["sunrise"].to_string()[-8:-3]}</b>\n'
        f'Зенит: <b>{time_day["zaval"].to_string()[-8:-3]}</b>\n'
        f'Последняя 1/3 ночи: <b>{tahadjud_time}</b>'
    )
    return daytime_message

def get_nextday_time(current_city):
    time_day = tat_table[(tat_table['city'] == current_city) & (tat_table['day'] == nextday_date.strftime('%Y.%m.%d'))]
    isha_time_th = current_date.strftime('%d.%m.%Y') + ' ' + time_day["isha"].to_string()[-8:]
    fajr_time_th = nextday_date.strftime('%d.%m.%Y') + ' ' + time_day["fajr"].to_string()[-8:]

    isha_time_dt = datetime.datetime.strptime(isha_time_th, '%d.%m.%Y %H:%M:%S')
    fajr_time_dt = datetime.datetime.strptime(fajr_time_th, '%d.%m.%Y %H:%M:%S')

    difference = (isha_time_dt - fajr_time_dt).total_seconds()
    current_sec = fajr_time_dt - timedelta(seconds=difference/-3)
    tahadjud_time = datetime.datetime.strftime(current_sec, '%H:%M')
    nextday_time_message = (
        f'🌍 Город: <b>{current_city}</b>\n\n'
        f'📅 Дата: <b>{nextday_date.strftime("%d.%m.%Y")}</b>\n\n'
        '🔭 Метод расчета: ДУМ РТ\n\n'
        f'Фаджр - <b>{time_day["fajr"].to_string()[-8:-3]}</b>\n'
        f'Фаджр в мечети - <b>{time_day["fajr_mosque"].to_string()[-8:-3]}</b>\n'
        f'Зухр - <b>{time_day["zuhr"].to_string()[-8:-3]}</b>\n'
        f'Аср - <b>{time_day["asr"].to_string()[-8:-3]}</b>\n'
        f'Магриб - <b>{time_day["magrib"].to_string()[-8:-3]}</b>\n'
        f'Иша - <b>{time_day["isha"].to_string()[-8:-3]}</b>\n\n'

        f'Рассвет: <b>{time_day["sunrise"].to_string()[-8:-3]}</b>\n'
        f'Зенит: <b>{time_day["zaval"].to_string()[-8:-3]}</b>\n'
        f'Последняя 1/3 ночи: <b>{tahadjud_time}</b>'
    )
    return nextday_time_message
