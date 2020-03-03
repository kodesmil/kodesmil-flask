import requests
from flask import Response, request
from functools import wraps

API_URL = 'http://localhost:5000'

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
            response_json = response.json()
            kwargs['user_id'] = response_json['inum']

            # check if user is authenticated
            if response.status_code != requests.codes.ok:
                return Response(
                    'Login required',
                    401,
                    {
                        'WWW-Authenticate': 'Basic realm="Login Required"',
                    },
                )

            # check if user has proper permissions, only if permissions were passed in decorator
            if permissions:
                for perm in permissions:
                    if perm not in response.json()['permissions']:
                        return Response(
                            'Permissions required',
                            401,
                            {
                                'WWW-Authenticate': 'Basic realm="Permissions Required"',
                            },
                        )

            return func(*args, **kwargs)

        return wrapper

    return real_decorator


def get_user_id(auth_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{}'.format(auth_token)
    }
    response = requests.get(INFO_URL, headers=headers).json()
    return response['inum']


# takes an endpoint and model owner field (eg. '/content/service' and 'provider')
# checks if user requesting to perform operations on data
# is this instance owner
# if an instance has no owner, then access is allowed by default

def check_ownership(endpoint, owner_field):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs, ):
            user_id = get_user_id(request.headers.get('Authorization'))
            headers = {
                'Content-Type': 'application/json',
                'Authorization': '{}'.format(request.headers.get('Authorization'))
            }
            response = requests.get(API_URL + endpoint + '/' + kwargs['instance_id'], headers=headers)

            if response.json()[owner_field] != user_id:
                return Response(
                    'Permissions required',
                    401,
                    {
                        'WWW-Authenticate': 'Basic realm="Permissions Required"'
                    }
                )
            elif response.json()[owner_field] is None:
                return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return real_decorator
