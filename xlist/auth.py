"""
Handles authentication for the api
"""

from flask import jsonify, make_response
from flask.ext.httpauth import HTTPBasicAuth
from settings import USERS as users

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    return users.get(username, None)

@auth.error_handler
def unauthorized():
    """
    Return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    """
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)
