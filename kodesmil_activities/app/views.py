from flask import Blueprint, jsonify, request
from flask_apispec import marshal_with, doc

from kodesmil_common.auth import require_auth_and_permissions, get_user_id
from .models import ActivitySchema
from .app import db

import requests

content = Blueprint('content', __name__)

# This is local IP of kodesmil_points container
# Can be checked using `docker inspect kodesmil_points_flask | grep "IPAddress"`
KODESMIL_POINTS_URL = 'http://172.21.0.2:5000/points'


# ping motim-points microservice about new data
def ping_points(token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{}'.format(token)
    }
    requests.post(
        KODESMIL_POINTS_URL,
        headers=headers,
    )


@doc(tags=['Activity'], description='')
@marshal_with(ActivitySchema())
@content.route('/activities', methods=['POST'])
@require_auth_and_permissions()
def add_activity():
    raw_data = request.get_json()
    raw_data['user_id'] = get_user_id(request.headers.get('Authorization'))
    instance = ActivitySchema().load(raw_data)
    db.activities.insert_one(instance)
    ping_points(request.headers.get('Authorization'))
    return '', 201


@doc(tags=['Activity'], description='')
@marshal_with(ActivitySchema())
@content.route('/activities', methods=['GET'])
@require_auth_and_permissions()
def get_last_activity():
    user_id = get_user_id(request.headers.get('Authorization'))
    schema = ActivitySchema()
    query = db.activities.find({'user_id': user_id}).sort('_id', -1).limit(1)
    instance = schema.dump(
        query[0]
    )
    return jsonify(instance)
