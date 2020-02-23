from flask import Blueprint, jsonify, request

from _utils.db import db_conn

from .models import *

sample_service = Blueprint('sample_service', __name__)
db = db_conn()


# REMEMBER to change routes, schema's names, function's names etc.


@sample_service.route('/sample_model')
def get_sample_models():
    schema = SampleModelSchema(many=True)
    sample_model = schema.dump(
        db.sample_model.find()
    )
    return jsonify(sample_model.data)


@sample_service.route('/sample_model', methods=['POST'])
def add_sample_models():
    sample_model = SampleModelSchema().load(request.get_json())
    db.services.insert_one(sample_model.data)
    return '', 204
