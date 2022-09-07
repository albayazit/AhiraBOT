from database import sqlite_bd

async def get_code(code):
	if list(code)[0] != 'E':
		if list(code)[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
			code = 'E' + str(code)
		elif list(code)[0] == 'e':
			code = code.replace('e', 'E', 1)
		elif list(code)[0] == 'Е':
			code = code.replace('Е', 'E', 1)
		elif list(code)[0] == 'е':
			code = code.replace('е', 'E', 1)

	id = sqlite_bd.cur.execute('SELECT code FROM halal_codes WHERE code == ?', (str(code), )).fetchone()[0]
	description = sqlite_bd.cur.execute('SELECT description FROM halal_codes WHERE code == ?', (str(code), )).fetchone()[0]
	permissiveness = sqlite_bd.cur.execute('SELECT permissiveness FROM halal_codes WHERE code == ?', (str(code), )).fetchone()[0]
	
	message = f'<b>Код:</b> {id}\n\n<b>Описание:</b> {description}\n\n<b>Дозволенность:</b> {permissiveness}'
	return message
