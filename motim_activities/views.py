from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
import datetime as dt
from flask_apispec import marshal_with, doc

from models import ActivitySchema
from app import db

from auth import require_auth_and_permissions, check_ownership

import requests

content = Blueprint('content', __name__)

MOTIM_POINTS_URL = 'http://localhost:5001/motim-points'

service_id_fields = [
    '_id',
    'category',
    'provider',
]

@doc(tags=['Activity'], description='')
@marshal_with(ActivitySchema())
@content.route('/motim-activity', methods=['POST'])
@require_auth_and_permissions()
def add_activity():
    instance = ActivitySchema().load(request.get_json())
    db.activities.insert_one(instance)

    # ping motim-points microservice about new data
    headers = {
        'Content-Type': 'application/json',
        'Authorization': '{}'.format(request.headers.get('Authorization'))
    }
    requests.get(
        MOTIM_POINTS_URL,
        headers=headers,
    )

    return '', 201