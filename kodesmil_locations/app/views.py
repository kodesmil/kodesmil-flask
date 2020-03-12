from flask import Blueprint, request
from flask_apispec import marshal_with, doc

from . import db
from .models import LocationSchema

content = Blueprint('content', __name__)


@doc(tags=['Location'], description='')
@marshal_with(LocationSchema())
@content.route('/locations', methods=['POST'])
def create_location(*args, **kwargs):
    request_data = request.get_json()
    result = db.locations.insert_one(LocationSchema().load(request_data))
    if result.acknowledged:
        return '', 201
    return '', 500
