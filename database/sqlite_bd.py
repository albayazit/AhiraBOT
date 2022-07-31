import sqlite3 as sq

def sql_start():
	global base, cur
	base = sq.connect('database.db')
	cur = base.cursor()
	if base:
		print('База данных подключена!')
	base.execute('CREATE TABLE IF NOT EXISTS favorite_other(user_id TEXT, address TEXT, method TEXT, school TEXT)')
	base.commit()