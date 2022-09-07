import pandas as pd
from database import sqlite_bd


data = pd.read_excel('data/halal/halal_food.xlsx')

async def scrap_food():
	try:
		sqlite_bd.cur.execute('SELECT name from halal_food').fetchall()[0]
	except:
		for i in range(0, 500):
			pd.set_option('display.max_colwidth', 500)
			current = data[data["ID"] == i]
			name = current["Название"].to_string(index = False)
			company = current["Компания"].to_string(index = False)
			period = current["Срок действия"].to_string(index = False)
			address = current["Адрес"].to_string(index = False)
			if name == 'Series([], )':
				pass
			else:
				sqlite_bd.cur.execute('INSERT INTO halal_food VALUES(?, ?, ?, ?)', (name, company, period, address))
				sqlite_bd.base.commit()
		print('База халяль заведений успешно загружена!')