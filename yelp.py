# config.py file ignored in git, get client keys from Yelp
import config
CLIENT_ID = config.CLIENT_ID()
CLIENT_SECRET = config.CLIENT_SECRET()

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

def writeData():
	# get a ton of data from various cities and write to data.txt
	# this will take a long time, but result in about 6700 restaurants
	data = {'data':[]}
	locations = ['Boston', 'New York', 'San Francisco', 'Austin', 'Los Angeles', 'Seattle', 'Washington DC', 'Philadelphia' \
	'Chicago', 'Houston', 'Phoenix', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Detroit', 'Portland', 'Memphis']

	for location in locations:
		for i in range(0,1000,50):
			json_data = searchRestaurants(i, location)
			for business in json_data["businesses"]:
				data['data'].append(business.copy())

	with open('data.txt', 'w+') as outfile:
		json.dump(data, outfile)

def searchRestaurants(offset, location):
	bis_url = 'https://api.yelp.com/v3/businesses/search'

	url_params = {
        'term': 'restaurants',
        'location': location.replace(' ', '+'),
        'offset': offset,
        'categories': 'restaurants'
    }

	return request(bis_url, token, url_params=url_params)

def analyzeFile():
	with open('data.txt', 'r') as f:
		array = json.load(f)

	unwanted = ['eventplanning', 'wedding_planning', 'catering', 'fooddeliveryservices', 'foodtrucks', 'vinyl_records'\
	'aquariums', 'jazzandblues', 'theater', 'movietheaters', 'gaybars']
	titleDict = {}
	data = []

	for business in array['data']:
		titleList = ""
		unwantedBool = False
		for cat in business["categories"]:
			title = cat["alias"]
			if(title in unwanted):
				unwantedBool = True
			titleList+=title+' '
			
		if(not unwantedBool):
			if(title in titleDict.keys()):
				titleDict[title]+=1
			else:
				titleDict[title]=1
			data.append(titleList)
	pickle.dump( data, open("titles.p", "wb"))

def analyzeFileML():
	data = pickle.load( open("titles.p", "rb"))

	from sklearn.feature_extraction.text import CountVectorizer
	cv = CountVectorizer()
	cv_fit=cv.fit_transform(data)
	print(cv.get_feature_names())
	print(cv_fit.toarray())
	


def categories():
	newdata = {'data':[]}
	with open('categories.json', 'r') as f:
		array = json.load(f)
	for cat in array:
		if any(i in cat["parents"] for i in ["restaurants"]):
			newdata['data'].append(cat)
	with open('shortcategories.txt', 'w+') as outfile:
		json.dump(newdata, outfile, indent=4)


# for flask request
def data(radius, lat, lng):
	cats = pickle.load( open("categories.p", "rb"))
	titleDict = {}
	for i in range(0,1000,50):
		json_data = searchLocalRestaurants(term='restaurants', limit=50, radius=radius, offset = i, lat=lat, lng=lng)
		for business in json_data["businesses"]:
			if(business['distance']>(40000.*radius/25.)):
				break
			#catmap maps each category with the number of occurences
			catmap = {}
			for category in business["categories"]:
				title = category["alias"]
				for cat in cats:
					if(title in cats[cat]):
						if(title in catmap.keys()):
							catmap[cat]+=1
						else:
							catmap[cat]=1
			if(len(catmap)!=0):
				title = max(catmap, key=catmap.get)
				if(title in titleDict.keys()):
					titleDict[title]+=1
				else:
					titleDict[title]=1
		else: #break out of nested for loop
			continue
		break
	return titleDict







