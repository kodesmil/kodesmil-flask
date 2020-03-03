from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
import datetime as dt
from flask_apispec import marshal_with, doc
from kodesmil_common.auth import require_auth_and_permissions, check_ownership

from .models import *
from .app import db

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
@content.route('/content/services', methods=['GET'])
@require_auth_and_permissions()
def get_services():
    schema = ServiceSchema(many=True)
    instances = schema.dump(
        db.services.find()
    )
    return jsonify(instances)


# return only one instance of data

@doc(tags=['Services'], description='')
@marshal_with(ServiceSchema(many=True))
@content.route('/content/services/<string:instance_id>', methods=['GET'])
@require_auth_and_permissions()
def get_service(instance_id):
    schema = ServiceSchema()

    instance = schema.dump(
        db.services.find_one({'_id': ObjectId(instance_id)})
    )

    return jsonify(instance)


# creates an instance

@doc(tags=['Services'], description='')
@marshal_with(ServiceSchema())
@content.route('/content/services', methods=['POST'])
@require_auth_and_permissions()
def add_service():
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())
    instance = ServiceSchema().load(request.get_json(raw_data))
    db.services.insert_one(instance)
    return '', 201


# replaces an instance with recieved data
# but, only if user is owner of this instance

@doc(tags=['Services'], description='')
@marshal_with(ServiceSchema())
@content.route('/content/services/<string:instance_id>', methods=['PUT'])
@require_auth_and_permissions()
@check_ownership('/content/services', 'provider')
def replace_service(instance_id):
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())
    instance = ServiceSchema().load(request.get_json(raw_data))
    result = db.services.replace_one({'_id': ObjectId(instance_id)}, instance)

    if not result.matched_count:
        raw_data['_id'] = ObjectId(instance_id)
        instance = ServiceSchema().load(request.get_json(raw_data))
        db.services.insert_one(instance)
        return '', 201

    return '', 204


# removes service instance

@doc(tags=['Services'], description='')
@marshal_with(ServiceSchema())
@content.route('/content/services/<string:instance_id>', methods=['DELETE'])
@require_auth_and_permissions()
@check_ownership('/content/services', 'provider')
def remove_service(instance_id):
    result = db.services.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200


# filter Services by anything you like, eg. id, category, provider etc.

@doc(tags=['Services'], description='')
@marshal_with(ServiceSchema(many=True))
@content.route('/content/services/filter')
@require_auth_and_permissions()
def filter_services():
    schema = ServiceSchema(many=True)

    if not request.json:
        instances = schema.dump(
            db.services.find()
        )
        return jsonify(instances)

    filters = {}
    for key in request.json:
        if key in service_id_fields:
            filters[key] = ObjectId(request.json[key])
        else:
            filters[key] = request.json[key]

    instances = schema.dump(
        db.services.find(filters)
    )
    return jsonify(instances)


# SERVICE CATEGORIES

@doc(tags=['Service Categories'], description='')
@marshal_with(ServiceCategorySchema(many=True))
@content.route('/content/service-categories', methods=['GET'])
@require_auth_and_permissions()
def get_service_categories():
    schema = ServiceCategorySchema(many=True)
    instances = schema.dump(
        db.service_categories.find()
    )
    return jsonify(instances)


# SERVICE PROVIDERS

@doc(tags=['Service Providers'], description='')
@marshal_with(ServiceProviderSchema(many=True))
@content.route('/content/service-providers', methods=['GET'])
@require_auth_and_permissions()
def get_service_providers():
    schema = ServiceProviderSchema(many=True)
    instances = schema.dump(
        db.service_providers.find()
    )
    return jsonify(instances)


@doc(tags=['Service Providers'], description='')
@marshal_with(ServiceProviderSchema())
@content.route('/content/service-providers/<string:instance_id>', methods=['GET'])
@require_auth_and_permissions()
def get_service_provider(instance_id):
    schema = ServiceProviderSchema()
    instance = schema.dump(
        db.service_providers.find_one({'_id': ObjectId(instance_id)})
    )
    return jsonify(instance)


@doc(tags=['Service Providers'], description='')
@marshal_with(ServiceProviderSchema())
@content.route('/content/service-providers', methods=['POST'])
@require_auth_and_permissions()
def add_service_provider():
    instance = ServiceProviderSchema().load(request.get_json())
    db.service_providers.insert_one(instance)
    return '', 204


@doc(tags=['Service Providers'], description='')
@marshal_with(ServiceProviderSchema())
@content.route('/content/service-providers/<string:instance_id>', methods=['PUT'])
@require_auth_and_permissions()
@check_ownership('/content/service-providers', 'owner_id')
def replace_service_provider(instance_id):
    raw_data = request.get_json()
    instance = ServiceProviderSchema().load(request.get_json(raw_data))
    result = db.service_providers.replace_one({'_id': ObjectId(instance_id)}, instance)

    if not result.matched_count:
        raw_data['_id'] = ObjectId(instance_id)
        instance = ServiceProviderSchema().load(request.get_json(raw_data))
        db.service_providers.insert_one(instance)
        return '', 201

    return '', 204


@doc(tags=['Service Providers'], description='')
@marshal_with(ServiceProviderSchema())
@content.route('/content/service-providers/<string:instance_id>', methods=['DELETE'])
@require_auth_and_permissions()
@check_ownership('/content/service-providers', 'owner_id')
def remove_service_provider(instance_id):
    result = db.service_providers.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200


# SERVICE SLOTS


@doc(tags=['Service Slots'], description='')
@marshal_with(ServiceSlotSchema(many=True))
@content.route('/content/service-slots', methods=['GET'])
@require_auth_and_permissions()
def get_service_slots():
    schema = ServiceSlotSchema(many=True)
    instances = schema.dump(
        db.service_slots.find()
    )
    return jsonify(instances)


@doc(tags=['Service Slots'], description='')
@marshal_with(ServiceSlotSchema())
@content.route('/content/service-slots/<string:instance_id>', methods=['GET'])
@require_auth_and_permissions()
def get_service_slot(instance_id):
    schema = ServiceSlotSchema()
    instance = schema.dump(
        db.service_slots.find_one({'_id': ObjectId(instance_id)})
    )
    return jsonify(instance)


@doc(tags=['Service Slots'], description='')
@marshal_with(ServiceSlotSchema())
@content.route('/content/service-slots', methods=['POST'])
@require_auth_and_permissions()
def add_service_slot():
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())
    instance = ServiceSlotSchema().load(raw_data)
    db.service_slots.insert_one(instance)
    return '', 204


# TODO both PUT and DELETE methods need another way to check ownership

@doc(tags=['Service Slots'], description='')
@marshal_with(ServiceSlotSchema())
@content.route('/content/service-slots/<string:instance_id>', methods=['PUT'])
@require_auth_and_permissions()
# @check_ownership('/content/service-providers', 'owner_id')
def replace_service_slot(instance_id):
    raw_data = request.get_json()
    instance = ServiceSlotSchema().load(request.get_json(raw_data))
    result = db.service_slots.replace_one({'_id': ObjectId(instance_id)}, instance)

    if not result.matched_count:
        raw_data['_id'] = ObjectId(instance_id)
        instance = ServiceSlotSchema().load(request.get_json(raw_data))
        db.service_slots.insert_one(instance)
        return '', 201

    return '', 204


@doc(tags=['Service Slots'], description='')
@marshal_with(ServiceProviderSchema())
@content.route('/content/service-slots/<string:instance_id>', methods=['DELETE'])
@require_auth_and_permissions()
# @check_ownership('/content/service-providers', 'owner_id')
def remove_service_slot(instance_id):
    result = db.service_slots.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200
