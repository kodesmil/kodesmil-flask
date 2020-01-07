import requests
from flask import Response, request
from functools import wraps


INFO_URL = 'https://auth.kodesmil.com/oxauth/restv1/userinfo'

# takes a list of permissions
# if empty, checks if user is logged in
# if not empty, additionally checks if user owns proper permission
# use as decorator


def require_auth_and_permissions(permissions=[]):
	def real_decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs, ):
			headers = {
				'Content-Type': 'application/json',
				'Authorization': '{}'.format(request.headers.get('Authorization'))
			}
			response = requests.get(INFO_URL, headers=headers)

			# check if user is authenticated
			if response.status_code != requests.codes.ok:
				return Response('Login required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

			# check if user has proper permissions, only if permissions were passed in decorator
			if permissions:
				for perm in permissions:
					if perm not in response.json()['permissions']:
						return Response('Permissions required', 401, {'WWW-Authenticate': 'Basic realm="Permissions Required"'})

			return func(*args, **kwargs)
		return wrapper
	return real_decorator
