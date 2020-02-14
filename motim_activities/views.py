from flask import Blueprint, jsonify, request
from flask_apispec import marshal_with, doc

from models import ActivitySchema
from app import db

from auth import require_auth_and_permissions, check_ownership, get_user_id

import requests

content = Blueprint('content', __name__)

# This is local IP of motim_points container
# Can be checked using `docker inspect motim_points_flask | grep "IPAddress"`
MOTIM_POINTS_URL = 'http://172.21.0.2:5000/motim-points'


# ping motim-points microservice about new data
def ping_points(token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{}'.format(token)
    }
    requests.post(
        MOTIM_POINTS_URL,
        headers=headers,
    )


@doc(tags=['Activity'], description='')
@marshal_with(ActivitySchema())
@content.route('/motim-activity', methods=['POST'])
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
@content.route('/motim-activity', methods=['GET'])
@require_auth_and_permissions()
def get_last_activity():
    user_id = get_user_id(request.headers.get('Authorization'))
    schema = ActivitySchema()
    query = db.activities.find({'user_id': user_id}).sort('_id', -1).limit(1)
    instance = schema.dump(
        query[0]
    )
    return jsonify(instance)
