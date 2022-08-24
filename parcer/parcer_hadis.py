import pandas as pd
import random

data = pd.read_excel('data/hadis/hadisi.xlsx')

async def get_hadis():
	count = random.randint(1, 205)
	hadis = data[data['id'] == count]['text'].to_string(index=False)
	return hadis