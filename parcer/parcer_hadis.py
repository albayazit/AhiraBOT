import pandas as pd
import random

data = pd.read_excel('data/hadis/hadisi.xlsx')

async def get_random_count():
	return random.randint(1, 205)

async def get_hadis(count):
	try:
		hadis = data['text'][count]
	except:
		hadis = data['text'][1]
	return hadis