from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
import datetime as dt
from flask_apispec import marshal_with, doc

from models import ActivityPointsSchema
from app import db

from auth import require_auth_and_permissions, check_ownership

import json

content = Blueprint('content', __name__)

MOTIM_ACTIVITY_URL = 'http://localhost:5000/motim-activity'


@doc(tags=['=Activity'], description='')
@marshal_with(ActivityPointsSchema())
@content.route('/motim-points', methods=['POST'])
@require_auth_and_permissions()
def add_activity():
    print('coootas')
    instance = ActivityPointsSchema().load(
        {
            'value': 100,
        }
    )
    db.points.insert_one(instance)

    return '', 200