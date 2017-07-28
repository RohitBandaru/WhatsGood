#!flask/bin/python
from flask import Flask, jsonify
import yelp

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/data/<int:radius>/<string:lat>/<string:lng>', methods=['GET'])
def data(radius, lng, lat):
	return jsonify(yelp.data(radius, float(lat), float(lng)))

@app.route('/data/<int:radius>/<string:lat>/<string:lng>', methods=['GET'])
def ratings(radius, lng, lat):
	return jsonify(yelp.data(radius, float(lat), float(lng)))


if __name__ == '__main__':
	app.run(debug=True)