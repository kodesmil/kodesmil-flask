from flask import Blueprint, request
from flask_apispec import marshal_with, doc
from kodesmil_common.auth import requires_auth

from .models import ActivityPointsSchema
from . import db

import requests

content = Blueprint('content', __name__)

# This is local IP of kodesmil_points container
# Can be checked using `docker inspect kodesmil_activities_flask | grep "IPAddress"`
KODESMIL_ACTIVITY_URL = 'http://172.21.0.2:5001/activities'


@doc(tags=['Activity'], description='')
@marshal_with(ActivityPointsSchema())
@content.route('/points', methods=['POST'])
@requires_auth
def add_new_points(*args, **kwargs):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{}'.format(request.headers.get('Authorization'))
    }
    response = requests.get(
        KODESMIL_ACTIVITY_URL,
        headers=headers,
    )

    json_response = response.json()
    user_id = kwargs['user_id']

    instance = ActivityPointsSchema().load(
        {
            'user_id': user_id,
            'value': json_response['value'],
            'activity_id': json_response['_id'],
        }
    )
    response = db.points.insert_one(instance)

    if response.acknowledged:
        return '', 201

    return '', 500


@doc(tags=['Activity'], description='')
@marshal_with(ActivityPointsSchema())
@content.route('/points', methods=['GET'])
@requires_auth
def get_points(*args, **kwargs):
    user_id = kwargs['user_id']
    schema = ActivityPointsSchema(many=True)
    instances = schema.dump(
        db.points.find({'user_id': user_id})
    )

    points = 0
    for instance in instances:
        points += instance['value']

    return {'points': points}
