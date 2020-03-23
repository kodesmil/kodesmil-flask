
#import requests
import json
import os
from functools import wraps
from flask import request, jsonify, _request_ctx_stack
#from flask_cors import cross_origin
from jose import jwt
from six.moves.urllib.request import urlopen

#API_URL = 'http://localhost:5000'
#INFO_URL = 'https://auth.kodesmil.com/oxauth/restv1/userinfo'

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_IDENTIFIER = os.environ['API_IDENTIFIER']
ALGORITHMS = ["RS256"]


# Format error response and append status code.
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Obtains the access token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({
            "code": "authorization_header_missing",
            "description": "Authorization header is expected",
        }, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with Bearer",
        }, 401)
    elif len(parts) == 1:
        raise AuthError({
            "code": "invalid_header",
            "description": "Token not found",
        }, 401)
    elif len(parts) > 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must be Bearer token",
        }, 401)

    token = parts[1]
    return token


def requires_scope(required_scope):
    """
    Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


def requires_auth(f):
    """
    Determines if the access token is valid
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthError({
                "code": "invalid_header",
                "description": "Invalid header. Use an RS256 signed JWT Access Token",
            }, 401)
        if unverified_header["alg"] == "HS256":
            raise AuthError({
                "code": "invalid_header",
                "description": "Invalid header. Use an RS256 signed JWT Access Token",
            }, 401)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({
                    "code": "token_expired",
                    "description": "token is expired",
                }, 401)
            except jwt.JWTClaimsError:
                raise AuthError({
                    "code": "invalid_claims",
                    "description": "incorrect claims, please check the audience and issuer",
                }, 401)
            except Exception:
                raise AuthError({
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                }, 401)

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError({
            "code": "invalid_header",
            "description": "Unable to find appropriate key",
        }, 401)
    return decorated


'''

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
    
'''
