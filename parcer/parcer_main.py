import requests

# get for day
def get_day_time(address, method, school):
	url = "https://aladhan.p.rapidapi.com/timingsByAddress"
	querystring = {"address":f"{address}","method":f"{method}","school":f"{school}"}

	headers = {
		"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
		"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	return response['data'][0]



# get for month

# url = "https://aladhan.p.rapidapi.com/calendarByAddress"

# querystring = {"address":"Казань","method":"2","school":"1"}

# headers = {
# 	"X-RapidAPI-Key": "fa3e8dc2dbmshd8f35322ed30bb0p1179d0jsn655fe6d43bde",
# 	"X-RapidAPI-Host": "aladhan.p.rapidapi.com"
# }

# response = requests.request("GET", url, headers=headers, params=querystring).json()

# print(response['data'][0]['timings']['Fajr'])