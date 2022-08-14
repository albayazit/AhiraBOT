import sqlite3 as sq

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