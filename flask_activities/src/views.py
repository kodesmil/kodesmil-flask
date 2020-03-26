from flask import Blueprint, jsonify, request
from flask_apispec import marshal_with, doc
from kodesmil_common.auth import requires_auth
from marshmallow import fields, ValidationError, missing

from kodesmil_common.user_schema import get_user
from . import db
from .fit.fit import get_heart_minutes, get_distances
from .models import ActivitySchema

import requests

from oauth2client.client import AccessTokenCredentials

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
@requires_auth
def add_activity(*args, **kwargs):
    raw_data = request.get_json()
    raw_data['user_id'] = kwargs['user_id']
    instance = ActivitySchema().load(raw_data)
    result = db.activities.insert_one(instance)

    if result.acknowledged:
        ping_points(request.headers.get('Authorization'))
        return '', 201

    return '', 500


@doc(tags=['Activity'], description='')
@marshal_with(ActivitySchema())
@content.route('/activities', methods=['GET'])
@requires_auth
def get_last_activity(*args, **kwargs):
    schema = ActivitySchema()
    query = db.activities.find({'user_id': kwargs['user_id']}).sort('_id', -1).limit(1)
    instance = schema.dump(
        query[0]
    )
    if not instance:
        return '', 404
    return jsonify(instance)


@doc(tags=['GoogleFitActivities'], description='')
@marshal_with(ActivitySchema())
@content.route('/sync/google-fit', methods=['POST'])
# @requires_auth
def add_google_fit_activity(*args, **kwargs):
    request_data = request.get_json()
    credentials = AccessTokenCredentials(request_data['access_token'], 'Flask/1.0')
    user = get_user(db, request_data)
    data = get_heart_minutes(credentials, user)
    data.extend(get_distances(credentials, user))
    activities = ActivitySchema(many=True).load(data)
    result = db.activities.insert_many(activities)
    if result.acknowledged:
        # ping_points(request.headers.get('Authorization'))
        return '', 201
    return '', 200
