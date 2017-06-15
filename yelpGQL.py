import yelp

#yelp.analyzeFile()

def request(url, token, url_params=None):
	url_params = url_params or {}
	headers = { 'Authorization': 'Bearer %s' % token, }
	response = requests.request('GET', url, headers=headers, params=url_params)

	return response.json()

def data():
	url = 'https://api.yelp.com/v3/graphql'

	

import graphene

class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.Argument(graphene.String, default_value="stranger"))

    def resolve_hello(self, args, context, info):
        return 'Hello ' + args['name']



print(type(yelp.token()))