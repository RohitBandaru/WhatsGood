CLIENT_ID = 'WMqiNkJ3XbQjLxHnZ2l8pQ'
CLIENT_SECRET = 'snC2xR229hBYTYQLCGzO8vFyXHOnnRhXyPR4NAN3U1jx0kFRj1dyOmAledvjJu9s'

import urllib.request as req
import urllib.parse as parse
import urllib.error
import json
import requests
import pickle

def token():
	url = 'https://api.yelp.com/oauth2/token'
	param = {"grant_type" : "client_credentials",
	"client_id":CLIENT_ID, "client_secret":CLIENT_SECRET}

	data = urllib.parse.urlencode(param).encode('ascii')
	req = urllib.request.Request(url, data)
	with urllib.request.urlopen(req) as response:
		page = response.read().decode('ascii')

	token = json.loads(page)["access_token"]

	return token

token = token()

def request(url, token, url_params=None):
	url_params = url_params or {}
	headers = { 'Authorization': 'Bearer %s' % token, }
	response = requests.request('GET', url, headers=headers, params=url_params)

	return response.json()

def searchRestaurants(term, limit, radius, offset, location):
	bis_url = 'https://api.yelp.com/v3/businesses/search'

	url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': 10
    }
	return request(bis_url, token, url_params=url_params)


def searchLocalRestaurants(term, limit, radius, offset, lat=None, lng=None):
	bis_url = 'https://api.yelp.com/v3/businesses/search'
	# radius in miles convert to m
	if(radius>25 or radius<0):
		print("radius exceeds limit, defaulting to 25 miles")
		radius = 25
	
	if(lat!=None and lng!=None):
		latitude = lat
		longitude = lng
	else:
		latitude = currentLocation()[0]
		longitude = currentLocation()[1]
	url_params = {
        'term': term.replace(' ', '+'),
        'latitude': latitude,
        'longitude': longitude,
        'limit': limit,
        'offset': offset,
        'radius': (int)(40000.*radius/25.) #max radius is 40 km or 25 mi
    }
	return request(bis_url, token, url_params=url_params)

def currentLocation():
	#returns (lat, lng) tuple
	#https://stackoverflow.com/questions/24906833/get-your-location-through-python
	send_url = 'http://freegeoip.net/json'
	r = requests.get(send_url)
	j = json.loads(r.text)
	lat = j['latitude']
	lon = j['longitude']
	return (lat,lon)

def restaurantStats():
	data = {'data':[]}
	titleDict = {}
	for i in range(0,100,50):
		json_data = searchLocalRestaurants(term='restaurants', limit=50, radius=25, offset = i,lat=None, lng=None)
		for business in json_data["businesses"]:
			if(business['distance']>1000):
				break
			data['data'].append(business.copy())
			title = business["categories"][0]["alias"]
			if(title in titleDict.keys()):
				titleDict[title]+=1
			else:
				titleDict[title]=1
	import json
	with open('data.txt', 'w+') as outfile:
		json.dump(data, outfile)
	return titleDict

def analyzeFile():
	with open('data.txt', 'r') as f:
		array = json.load(f)

	unwanted = ['eventplanning', 'wedding_planning', 'catering', 'fooddeliveryservices']
	titleDict = {}
	data = []
	for business in array['data']:
		if business["categories"][0]['alias'] not in unwanted:
			titleList = []
			for cat in business["categories"]:
				title = cat["alias"]
				titleList.append(title)
				if(title in titleDict.keys()):
					titleDict[title]+=1
				else:
					titleDict[title]=1
			data.append(titleList)

	return titleDict

def categories():
	newdata = {'data':[]}
	with open('categories.json', 'r') as f:
		array = json.load(f)
	for cat in array:
		if any(i in cat["parents"] for i in ["restaurants"]):
			newdata['data'].append(cat)
	with open('shortcategories.txt', 'w+') as outfile:
		json.dump(newdata, outfile, indent=4)

def data(radius, lat, lng):
	titleDict = {}
	for i in range(0,1000,50):
		json_data = searchLocalRestaurants(term='restaurants', limit=50, radius=radius, offset = i, lat=lat, lng=lng)
		for business in json_data["businesses"]:
			if(business['distance']>(40000.*radius/25.)):
				break
			title = business["categories"][0]["alias"]

			if(title in titleDict.keys()):
				titleDict[title]+=1
			else:
				titleDict[title]=1
	return titleDict

#print(data(10, 42.5879,-72.3498))


