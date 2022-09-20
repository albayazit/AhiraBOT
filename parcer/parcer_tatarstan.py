# парсим время намаза для Татарстана с excel
from datetime import datetime, timedelta
import calendar
import pandas as pd
import datetime

tat_table = pd.read_excel('data/namaz/namaz_time_tatarstan.xlsx')
all_cities = tat_table['city'].unique()
tat_table['day'] = tat_table['day'].dt.strftime('%Y.%m.%d')

# get time from excel
async def get_time(current_city, period):
    today = datetime.date.today()
    nextday = today + datetime.timedelta(days=1)
    cl = calendar.Calendar()
    if period == 'today':
        times_for_day = tat_table[(tat_table['city'] == current_city) & (tat_table['day'] == today.strftime('%Y.%m.%d'))]
        isha_time = datetime.datetime.strptime(today.strftime('%d.%m.%Y') + ' ' + times_for_day["isha"].to_string()[-8:], '%d.%m.%Y %H:%M:%S')
        fajr_time = datetime.datetime.strptime(nextday.strftime('%d.%m.%Y') + ' ' + times_for_day["fajr"].to_string()[-8:], '%d.%m.%Y %H:%M:%S')
        seconds_in_tahad = fajr_time - timedelta(seconds=(isha_time - fajr_time).total_seconds()/-3)
        tahadjud_time = datetime.datetime.strftime(seconds_in_tahad, '%H:%M')

        daytime_message = (
        f'🌍 Город: <b>{current_city}</b>\n\n'
        f'📅 Дата: <b>{today.strftime("%d.%m.%Y")}</b>\n\n'
        '🔭 Метод расчета: <b>ДУМ РТ</b>\n\n'
        f'Фаджр - <b>{times_for_day["fajr"].to_string()[-8:-3]}</b>\n'
        f'Фаджр в мечети - <b>{times_for_day["fajr_mosque"].to_string()[-8:-3]}</b>\n'
        f'Зухр - <b>{times_for_day["zuhr"].to_string()[-8:-3]}</b>\n'
        f'Аср - <b>{times_for_day["asr"].to_string()[-8:-3]}</b>\n'
        f'Магриб - <b>{times_for_day["magrib"].to_string()[-8:-3]}</b>\n'
        f'Иша - <b>{times_for_day["isha"].to_string()[-8:-3]}</b>\n\n'
        
        f'Рассвет: <b>{times_for_day["sunrise"].to_string()[-8:-3]}</b>\n'
        f'Зенит: <b>{times_for_day["zaval"].to_string()[-8:-3]}</b>\n'
        f'Последняя 1/3 ночи: <b>{tahadjud_time}</b>'
        )
    elif period == 'tomorrow':
        times_for_day = tat_table[(tat_table['city'] == current_city) & (tat_table['day'] == nextday.strftime('%Y.%m.%d'))]
        isha_time = datetime.datetime.strptime(today.strftime('%d.%m.%Y') + ' ' + times_for_day["isha"].to_string()[-8:], '%d.%m.%Y %H:%M:%S')
        fajr_time = datetime.datetime.strptime(nextday.strftime('%d.%m.%Y') + ' ' + times_for_day["fajr"].to_string()[-8:], '%d.%m.%Y %H:%M:%S')
        seconds_in_tahad = fajr_time - timedelta(seconds=(isha_time - fajr_time).total_seconds()/-3)
        tahadjud_time = datetime.datetime.strftime(seconds_in_tahad, '%H:%M')

        daytime_message = (
        f'🌍 Город: <b>{current_city}</b>\n\n'
        f'📅 Дата: <b>{nextday.strftime("%d.%m.%Y")}</b>\n\n'
        '🔭 Метод расчета: <b>ДУМ РТ</b>\n\n'
        f'Фаджр - <b>{times_for_day["fajr"].to_string()[-8:-3]}</b>\n'
        f'Фаджр в мечети - <b>{times_for_day["fajr_mosque"].to_string()[-8:-3]}</b>\n'
        f'Зухр - <b>{times_for_day["zuhr"].to_string()[-8:-3]}</b>\n'
        f'Аср - <b>{times_for_day["asr"].to_string()[-8:-3]}</b>\n'
        f'Магриб - <b>{times_for_day["magrib"].to_string()[-8:-3]}</b>\n'
        f'Иша - <b>{times_for_day["isha"].to_string()[-8:-3]}</b>\n\n'
        
        f'Рассвет: <b>{times_for_day["sunrise"].to_string()[-8:-3]}</b>\n'
        f'Зенит: <b>{times_for_day["zaval"].to_string()[-8:-3]}</b>\n'
        f'Последняя 1/3 ночи: <b>{tahadjud_time}</b>'
        )
    else:
        period_datetime = datetime.datetime.strptime(period, '%Y.%m.%d')
        times_for_day = tat_table[(tat_table['city'] == current_city) & (tat_table['day'] == period_datetime.strftime('%Y.%m.%d'))]
        isha_time = datetime.datetime.strptime(period_datetime.strftime('%d.%m.%Y') + ' ' + times_for_day["isha"].to_string()[-8:], '%d.%m.%Y %H:%M:%S')
        fajr_time = datetime.datetime.strptime((period_datetime + datetime.timedelta(days=1)).strftime('%d.%m.%Y') + ' ' + times_for_day["fajr"].to_string()[-8:], '%d.%m.%Y %H:%M:%S')
        seconds_in_tahad = fajr_time - timedelta(seconds=(isha_time - fajr_time).total_seconds()/-3)
        tahadjud_time = datetime.datetime.strftime(seconds_in_tahad, '%H:%M')

        daytime_message = (
        f'🌍 Город: <b>{current_city}</b>\n\n'
        f'📅 Дата: <b>{period_datetime.strftime("%d.%m.%Y")}</b>\n\n'
        '🔭 Метод расчета: <b>ДУМ РТ</b>\n\n'
        f'Фаджр - <b>{times_for_day["fajr"].to_string()[-8:-3]}</b>\n'
        f'Фаджр в мечети - <b>{times_for_day["fajr_mosque"].to_string()[-8:-3]}</b>\n'
        f'Зухр - <b>{times_for_day["zuhr"].to_string()[-8:-3]}</b>\n'
        f'Аср - <b>{times_for_day["asr"].to_string()[-8:-3]}</b>\n'
        f'Магриб - <b>{times_for_day["magrib"].to_string()[-8:-3]}</b>\n'
        f'Иша - <b>{times_for_day["isha"].to_string()[-8:-3]}</b>\n\n'
        
        f'Рассвет: <b>{times_for_day["sunrise"].to_string()[-8:-3]}</b>\n'
        f'Зенит: <b>{times_for_day["zaval"].to_string()[-8:-3]}</b>\n'
        f'Последняя 1/3 ночи: <b>{tahadjud_time}</b>'
        )
    return daytime_message
