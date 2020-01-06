import requests
from flask import Flask, Response, request

from functools import wraps


INFO_URL = 'https://auth.kodesmil.com/oxauth/restv1/userinfo'


def auth(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		headers = {
			'Content-Type': 'application/json',
			'Authorization': '{}'.format(request.headers.get('Authorization'))
		}
		response = requests.get(INFO_URL, headers=headers)
		if response.status_code == requests.codes.ok:
			return func(*args, **kwargs)
		return Response('plz login', 401, {'WWW-Authenticate':'Basic realm="Login Required"'})
	return wrapper


# this function returns current users attribute from Gluu DB, based on sent auth token
# OR, it returns if user is authenticated, if
# TODO change to wrapper


def get_user_attribute(auth_token, attribute):
	headers = {
		'Content-Type': 'application/json',
		'Authorization': '{}'.format(auth_token)
	}

	response = requests.request("POST", INFO_URL, headers=headers).json()
	return response[attribute]
