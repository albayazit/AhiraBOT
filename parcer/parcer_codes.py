import pandas as pd

data = pd.read_excel('data/halal/halal_list.xlsx')


async def get_code(code):
	if list(code)[0] != 'E':
		code = 'E'+str(code)
	info = data[data['Код'] == code]
	message = f'''
		Код: {info['Код']}\n
		Описание: {info['Описание']}\n
		Дозволенность: {info['Дозволенность']}
	'''
	return message
