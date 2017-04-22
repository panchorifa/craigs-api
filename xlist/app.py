"""
xlist API
"""
import traceback
import json
from flask import Flask, jsonify, request
from auth import auth
from services import XlistService
from cache import Cache
from settings import CACHE_DIRECTORY


app = Flask(__name__, static_url_path='')
cache = Cache(CACHE_DIRECTORY)
service = XlistService(cache)


@app.route('/categories', methods=['GET'])
# @auth.login_required
def get_categories():
    """
    List of craigslist categories

    :statuscode 200: no error
    :statuscode 403: invalid creds
    """
    try:
        _cats = service.categories()
        return jsonify({'categories': _cats})
    except Exception, e:
        traceback.print_exc()


@app.route('/<region>/cities', methods=['GET'])
# @auth.login_required
def get_cities(region):
    """
    List of craigslist cities

    :statuscode 200: no error
    :statuscode 403: invalid creds
    """
    try:
        _cities = service.cities(region)
        return jsonify({'cities': _cities.json()})
    except Exception, e:
        traceback.print_exc()


@app.route('/cities/<city>/<cat>', methods=['GET'])
# @auth.login_required
def get_items(city, cat):
    """
    List of craigslist items

    :statuscode 200: no error
    :statuscode 403: invalid creds
    """
    try:
        keys = request.args.get('k', '').split(',')
        items = service.find_by_city(city, cat, keys)
    	return jsonify({'response': items.json()})
    except Exception, e:
        traceback.print_exc()


@app.before_request
def option_autoreply():
    """
    Always reply 200 on OPTIONS request
    """
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        resp_headers = resp.headers

        # Allow the origin which made the XHR
        resp_headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        resp_headers['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        resp_headers['Access-Control-Max-Age'] = "10"

        # keep current headers
        if headers is not None:
            resp_headers['Access-Control-Allow-Headers'] = headers
        return resp


@app.after_request
def set_allow_origin(resp):
    """
    Set origin for GET, POST, PUT, DELETE requests
    """
    resp_headers = resp.headers
    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        resp_headers['Access-Control-Allow-Origin'] = request.headers['Origin']
    return resp
