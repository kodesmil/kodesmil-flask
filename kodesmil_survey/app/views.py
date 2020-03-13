from flask import Blueprint, request, jsonify
from flask_apispec import marshal_with, doc
from kodesmil_common.auth import requires_auth
from kodesmil_common.user_schema import get_user

from . import db
from .models import AnswerSchema, QuestionSchema

content = Blueprint('content', __name__)


@doc(tags=['Answer'], description='')
@marshal_with(AnswerSchema())
@content.route('/answers', methods=['POST'])
@requires_auth
def create_answer(*args, **kwargs):
    request_data = request.get_json()
    user = get_user(db, kwargs['user_id'])
    request_data['author_id'] = user['_id']
    result = db.answers.insert_one(AnswerSchema().load(request_data))
    if result.acknowledged:
        return '', 201
    return '', 500


@doc(tags=['Answer'], description='')
@marshal_with(AnswerSchema())
@content.route('/answers', methods=['GET'])
@requires_auth
def get_answers(*args, **kwargs):
    user = get_user(db, kwargs['user_id'])
    answers = db.answers \
        .find({'user_id': user['_user:id']}) \
        .sort('_id', -1) \
        .limit(1)
    return jsonify(AnswerSchema().dump(
        answers, many=True
    )), 200


@doc(tags=['Question'], description='')
@marshal_with(QuestionSchema())
@content.route('/questions', methods=['GET'])
def get_questions(*args, **kwargs):
    return jsonify(QuestionSchema().dump(
        db.questions.find(), many=True,
    )), 200
