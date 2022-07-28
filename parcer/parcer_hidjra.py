# парсим дату по хиджре
import requests
from bs4 import BeautifulSoup

headers = {
	'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37'
}

url = 'https://azan.kz/'
try:
	responce = requests.get(url=url, headers=headers).text
except:
	print('Scrapping ERROR')
soup = BeautifulSoup(responce, 'lxml')

def main():
	try:
		for item in soup.find_all('div', class_='widget-cell'):
			if len(item['class']) != 1:
				continue
			else:
				return item.text
				break
	except:
		print('Item not founded')