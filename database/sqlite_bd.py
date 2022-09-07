import sqlite3 as sq
import pandas as pd

def sql_start():
	global base, cur
	base = sq.connect('database.db')
	cur = base.cursor()
	if base:
		print('База данных подключена!')
	base.execute('CREATE TABLE IF NOT EXISTS favorite_other(user_id TEXT, address TEXT,school TEXT)')
	base.commit()
	base.execute('CREATE TABLE IF NOT EXISTS favorite_tatarstan(user_id TEXT, address TEXT)')
	base.commit()
	base.execute('CREATE TABLE IF NOT EXISTS favorite_kazakhstan(user_id TEXT, address TEXT)')
	base.commit()
	base.execute('CREATE TABLE IF NOT EXISTS favorite_dagestan(user_id TEXT, address TEXT)')
	base.commit()
	base.execute('CREATE TABLE IF NOT EXISTS tracker(user_id TEXT, fajr TEXT, fajr_need TEXT, zuhr TEXT, zuhr_need TEXT, asr TEXT, asr_need TEXT, magrib TEXT, magrib_need TEXT, isha TEXT, isha_need TEXT, vitr TEXT, vitr_need TEXT, first_date TEXT, second_date TEXT)')
	base.commit()
	base.execute('CREATE TABLE IF NOT EXISTS zikr(user_id TEXT, zikr_1_today TEXT, zikr_1_all, zikr_2_today TEXT, zikr_2_all, zikr_3_today TEXT, zikr_3_all, zikr_4_today TEXT, zikr_4_all, zikr_5_today TEXT, zikr_5_all, zikr_6_today TEXT, zikr_6_all, zikr_7_today TEXT, zikr_7_all, zikr_8_today TEXT, zikr_8_all, zikr_9_today TEXT, zikr_9_all, zikr_10_today TEXT, zikr_10_all, zikr_11_today TEXT, zikr_11_all, zikr_12_today TEXT, zikr_12_all, zikr_13_today TEXT, zikr_13_all, zikr_14_today TEXT, zikr_14_all, zikr_15_today TEXT, zikr_15_all, zikr_16_today TEXT, zikr_16_all)')
	base.commit()
	base.execute('CREATE TABLE IF NOT EXISTS hadis(user_id TEXT, hadis_id TEXT, id TEXT)')
	base.commit()
	base.execute('CREATE TABLE IF NOT EXISTS halal_codes(code TEXT, description TEXT, permissiveness TEXT)')
	base.commit()
	base.execute('CREATE TABLE IF NOT EXISTS halal_food(name TEXT, company TEXT, period TEXT, address TEXT)')
	base.commit()