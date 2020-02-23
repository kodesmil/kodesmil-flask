from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
import datetime as dt
from flask_apispec import marshal_with, doc

from models import ActivityPointsSchema
from app import db

from auth import require_auth_and_permissions, check_ownership, get_user_id

import requests

content = Blueprint('content', __name__)

# This is local IP of motim_points container
# Can be checked using `docker inspect motim_activities_flask | grep "IPAddress"`
MOTIM_ACTIVITY_URL = 'http://172.21.0.2:5001/motim-activity'


@doc(tags=['Activity'], description='')
@marshal_with(ActivityPointsSchema())
@content.route('/motim-points', methods=['POST'])
@require_auth_and_permissions()
def add_new_points():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{}'.format(request.headers.get('Authorization'))
    }
    response = requests.get(
        MOTIM_ACTIVITY_URL,
        headers=headers,
    )

    json_response = response.json()
    user_id = get_user_id(request.headers.get('Authorization'))

    instance = ActivityPointsSchema().load(
        {
            'user_id': user_id,
            'value': json_response['value'],
            'activity_id': ObjectId(json_response['_id']),
        }
    )
    db.points.insert_one(instance)

    return '', 201


@doc(tags=['Activity'], description='')
@marshal_with(ActivityPointsSchema())
@content.route('/motim-points', methods=['GET'])
@require_auth_and_permissions()
def get_points():
    user_id = get_user_id(request.headers.get('Authorization'))
    schema = ActivityPointsSchema(many=True)
    instances = schema.dump(
        db.points.find({'user_id': user_id})
    )

    points = 0
    for instance in instances:
        points += instance['value']

    return {'points': points}
