import sqlite3 as sq

def sql_start():
	global base, cur
	base = sq.connect('database.db')
	cur = base.cursor()
	if base:
		print('База данных подключена!')
	base.execute('CREATE TABLE IF NOT EXISTS cities(city_id TEXT, user_id TEXT, city TEXT)')
	base.commit()