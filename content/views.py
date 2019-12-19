from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
import datetime as dt
from flask_apispec import marshal_with, doc

from models import *
import views

content = Blueprint('content', __name__)

service_id_fields = [
    '_id',
    'category',
    'provider'
]

# SERVICES

# returns every Service instances in DB


@doc(tags=['Services'], description='')
@marshal_with(ServiceSchema(many=True))
@content.route('/content/services')
def get_services():
    schema = ServiceSchema(many=True)
    instances = schema.dump(
        db.services.find()
    )
    return jsonify(instances.data)


@doc(tags=['Services'], description='')
@marshal_with(ServiceSchema())
@content.route('/content/services', methods=['POST'])
def add_service():
    raw_data = request.get_json()
    raw_data['updated_at'] = dt.datetime.now()
    instance = ServiceSchema().load(request.get_json(raw_data))
    db.services.insert_one(instance.data)
    return '', 204


# filter Services by anything you like, eg. id, category, provider etc.

@doc(tags=['Services'], description='')
@marshal_with(ServiceSchema(many=True))
@content.route('/content/services/filter')
def filter_services():
    schema = ServiceSchema(many=True)

    if not request.json:
        instances = schema.dump(
            db.services.find()
        )
        return jsonify(instances.data)

    filters = {}
    for key in request.json:
        if key in service_id_fields:
            filters[key] = ObjectId(request.json[key])
        else:
            filters[key] = request.json[key]

    instances = schema.dump(
        db.services.find(filters)
    )
    return jsonify(instances.data)


# SERVICE CATEGORIES

@doc(tags=['Service Categories'], description='')
@marshal_with(ServiceCategorySchema(many=True))
@content.route('/content/service-categories')
def get_service_categories():
    schema = ServiceCategorySchema(many=True)
    instances = schema.dump(
        db.service_categories.find()
    )
    return jsonify(instances.data)


@doc(tags=['Service Categories'], description='')
@marshal_with(ServiceCategorySchema())
@content.route('/content/service-categories', methods=['POST'])
def add_service_category():
    instance = ServiceCategorySchema().load(request.get_json())
    db.service_categories.insert_one(instance.data)
    return '', 204


# SERVICE PROVIDERS


@doc(tags=['Service Providers'], description='')
@marshal_with(ServiceProviderSchema(many=True))
@content.route('/content/service-providers')
def get_service_providers():
    schema = ServiceProviderSchema(many=True)
    instances = schema.dump(
        db.service_providers.find()
    )
    return jsonify(instances.data)


@doc(tags=['Service Providers'], description='')
@marshal_with(ServiceProviderSchema())
@content.route('/content/service-providers', methods=['POST'])
def add_service_provider():
    instance = ServiceProviderSchema().load(request.get_json())
    db.service_providers.insert_one(instance.data)
    return '', 204


# SERVICE SLOTS


@doc(tags=['Service Slots'], description='')
@marshal_with(ServiceSlotSchema(many=True))
@content.route('/content/service-slots')
def get_service_slots():
    schema = ServiceSlotSchema(many=True)
    instances = schema.dump(
        db.service_slots.find()
    )
    return jsonify(instances.data)


@doc(tags=['Service Slots'], description='')
@marshal_with(ServiceSlotSchema())
@content.route('/content/service-slots', methods=['POST'])
def add_service_slot():
    raw_data = request.get_json()
    raw_data['updated_at'] = dt.datetime.now()
    instance = ServiceSlotSchema().load(raw_data)
    db.service_slots.insert_one(instance.data)
    return '', 204
