import datetime as dt

from flask import Blueprint, jsonify, request
from flask_apispec import marshal_with, doc
from kodesmil_common.auth import requires_auth

from . import db
from .models import SurveyRankSchema, UserSchema

content = Blueprint('content', __name__)


@doc(tags=['Ranks'], description='')
@marshal_with(SurveyRankSchema())
@content.route('/ranks', methods=['POST'])
# @requires_auth
def add_rank(*args, **kwargs):
    request_data = request.get_json()
    user = get_user(request_data)
    request_data['_user_id'] = user['_id']
    # to remove
    request_data.pop('email', None)
    result = db.ranks.insert_one(SurveyRankSchema().load(request_data))
    if result.acknowledged:
        return '', 201
    return '', 500


@doc(tags=['Ranks'], description='')
@marshal_with(SurveyRankSchema())
@content.route('/ranks', methods=['GET'])
# @requires_auth
def get_ranks(*args, **kwargs):
    request_data = request.get_json()
    user = get_user(request_data)
    ranks = db.ranks \
        .find({'user_id': user['_user:id']}) \
        .sort('_id', -1) \
        .limit(1)
    return SurveyRankSchema().dump(
        ranks, many=True
    ), 200


def get_user(request_data):
    email = request_data['email']
    match = {'email': email}
    user = db.users.find_one(match)
    user_schema = UserSchema().load({
        'email': email,
        'last_synced_at': dt.datetime.now().isoformat(),
    })
    if not user:
        db.users.insert_one(user_schema)
        return db.users.find_one(match)
    else:
        db.users.replace_one(
            match,
            user_schema,
            True,
        )
        return db.users.find_one(match)
