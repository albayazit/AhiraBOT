import pandas as pd
from database import sqlite_bd
	
data = pd.read_excel('data/halal/halal_list.xlsx')

async def scrap_codes():
	try:
		sqlite_bd.cur.execute('SELECT code FROM halal_codes WHERE code == ?', ('E100', )).fetchone()[0]
	except:
		for i in range(100, 1000):
			pd.set_option('display.max_colwidth', 500)
			info = data[data['Код'] == 'E'+str(i)]
			info['Дозволенность'] = info['Дозволенность'].str.replace(r'\n', '')
			info['Описание'] = info['Описание'].str.replace(r'\n', '')
			code = info["Код"].to_string(index = False)
			description = info["Описание"].to_string(index = False)
			permissiveness = info["Дозволенность"].to_string(index = False)
			if code[0] == 'E':
				sqlite_bd.cur.execute('INSERT INTO halal_codes VALUES(?, ?, ?)', (code, description, permissiveness))
				sqlite_bd.base.commit()
			else:
				pass

		print('База E-кодов успешно загружена!')