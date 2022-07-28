import sqlite3 as sq

def sql_start():
	global base, cur
	base = sq.connect('ahira_users.db')
	cur = base.cursor()
	if base:
		print('База данных подключена!')
	base.execute('CREATE TABLE IF NOT EXISTS user(user_id TEXT PRIMARY KEY, city TEXT)')
	base.commit()

