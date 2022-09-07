from database import sqlite_bd

async def get_message(page):
	key = page * 5
	message = ''
	try:
		for i in range(key - 5, key):
			id = sqlite_bd.cur.execute('SELECT id FROM halal_food WHERE id == ?', (i+1, )).fetchone()[0]
			name = sqlite_bd.cur.execute('SELECT name FROM halal_food WHERE id == ?', (i+1, )).fetchone()[0]
			company = sqlite_bd.cur.execute('SELECT company FROM halal_food WHERE id == ?', (i+1, )).fetchone()[0]
			period = sqlite_bd.cur.execute('SELECT period FROM halal_food WHERE id == ?', (i+1, )).fetchone()[0]
			address = sqlite_bd.cur.execute('SELECT address FROM halal_food WHERE id == ?', (i+1, )).fetchone()[0]

			message += f'{id}. {name}\n{company}\n{period}\n{address}\n\n'
	except:
		pass
	return message
