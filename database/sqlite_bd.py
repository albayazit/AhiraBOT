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