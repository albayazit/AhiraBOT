import pandas as pd
import random

data = pd.read_excel('data/hadis/hadisi.xlsx')

async def get_random_count():
	return random.randint(1, 205)

async def get_hadis(count):
	hadis = data['text'][count]
	return hadis