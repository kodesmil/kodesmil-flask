from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
import datetime as dt
from flask_apispec import marshal_with, doc
from kodesmil_common.auth import require_auth_and_permissions, check_ownership

from .models import *
from .app import db

content = Blueprint('content', __name__)

product_id_fields = [
    '_id',
    'category',
    'provider'
]


# PRODUCTS

# returns every Product instances in DB

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema(many=True))
@content.route('/content/products', methods=['GET'])
@require_auth_and_permissions()
def get_products():
    schema = ProductSchema(many=True)
    instances = schema.dump(
        db.products.find()
    )
    return jsonify(instances)


# return only one instance of data

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema(many=True))
@content.route('/content/products/<string:instance_id>', methods=['GET'])
@require_auth_and_permissions()
def get_product(instance_id):
    schema = ProductSchema()

    instance = schema.dump(
        db.products.find_one({'_id': ObjectId(instance_id)})
    )

    return jsonify(instance)


# creates an instance

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema())
@content.route('/content/products', methods=['POST'])
@require_auth_and_permissions()
def add_product():
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())
    instance = ProductSchema().load(request.get_json(raw_data))
    db.products.insert_one(instance)
    return '', 201


# replaces an instance with recieved data
# but, only if user is owner of this instance

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema())
@content.route('/content/products/<string:instance_id>', methods=['PUT'])
@require_auth_and_permissions()
@check_ownership('/content/products', 'provider')
def replace_product(instance_id):
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())
    instance = ProductSchema().load(request.get_json(raw_data))
    result = db.products.replace_one({'_id': ObjectId(instance_id)}, instance)

    if not result.matched_count:
        raw_data['_id'] = ObjectId(instance_id)
        instance = ProductSchema().load(request.get_json(raw_data))
        db.products.insert_one(instance)
        return '', 201

    return '', 204


# removes product instance

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema())
@content.route('/content/products/<string:instance_id>', methods=['DELETE'])
@require_auth_and_permissions()
@check_ownership('/content/products', 'provider')
def remove_product(instance_id):
    result = db.products.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200


# filter Products by anything you like, eg. id, category, provider etc.

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema(many=True))
@content.route('/content/products/filter')
@require_auth_and_permissions()
def filter_products():
    schema = ProductSchema(many=True)

    if not request.json:
        instances = schema.dump(
            db.products.find()
        )
        return jsonify(instances)

    filters = {}
    for key in request.json:
        if key in product_id_fields:
            filters[key] = ObjectId(request.json[key])
        else:
            filters[key] = request.json[key]

    instances = schema.dump(
        db.products.find(filters)
    )
    return jsonify(instances)


# PRODUCT CATEGORIES

@doc(tags=['Product Categories'], description='')
@marshal_with(ProductCategorySchema(many=True))
@content.route('/content/product-categories', methods=['GET'])
@require_auth_and_permissions()
def get_product_categories():
    schema = ProductCategorySchema(many=True)
    instances = schema.dump(
        db.product_categories.find()
    )
    return jsonify(instances)


# PRODUCT PROVIDERS

@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema(many=True))
@content.route('/content/product-providers', methods=['GET'])
@require_auth_and_permissions()
def get_product_providers():
    schema = ProductProviderSchema(many=True)
    instances = schema.dump(
        db.product_providers.find()
    )
    return jsonify(instances)


@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema())
@content.route('/content/product-providers/<string:instance_id>', methods=['GET'])
@require_auth_and_permissions()
def get_product_provider(instance_id):
    schema = ProductProviderSchema()
    instance = schema.dump(
        db.product_providers.find_one({'_id': ObjectId(instance_id)})
    )
    return jsonify(instance)


@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema())
@content.route('/content/product-providers', methods=['POST'])
@require_auth_and_permissions()
def add_product_provider():
    instance = ProductProviderSchema().load(request.get_json())
    db.product_providers.insert_one(instance)
    return '', 204


@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema())
@content.route('/content/product-providers/<string:instance_id>', methods=['PUT'])
@require_auth_and_permissions()
@check_ownership('/content/product-providers', 'owner_id')
def replace_product_provider(instance_id):
    raw_data = request.get_json()
    instance = ProductProviderSchema().load(request.get_json(raw_data))
    result = db.product_providers.replace_one({'_id': ObjectId(instance_id)}, instance)

    if not result.matched_count:
        raw_data['_id'] = ObjectId(instance_id)
        instance = ProductProviderSchema().load(request.get_json(raw_data))
        db.product_providers.insert_one(instance)
        return '', 201

    return '', 204


@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema())
@content.route('/content/product-providers/<string:instance_id>', methods=['DELETE'])
@require_auth_and_permissions()
@check_ownership('/content/product-providers', 'owner_id')
def remove_product_provider(instance_id):
    result = db.product_providers.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200


# PRODUCT SLOTS


@doc(tags=['Product Slots'], description='')
@marshal_with(ProductSlotSchema(many=True))
@content.route('/content/product-slots', methods=['GET'])
@require_auth_and_permissions()
def get_product_slots():
    schema = ProductSlotSchema(many=True)
    instances = schema.dump(
        db.product_slots.find()
    )
    return jsonify(instances)


@doc(tags=['Product Slots'], description='')
@marshal_with(ProductSlotSchema())
@content.route('/content/product-slots/<string:instance_id>', methods=['GET'])
@require_auth_and_permissions()
def get_product_slot(instance_id):
    schema = ProductSlotSchema()
    instance = schema.dump(
        db.product_slots.find_one({'_id': ObjectId(instance_id)})
    )
    return jsonify(instance)


@doc(tags=['Product Slots'], description='')
@marshal_with(ProductSlotSchema())
@content.route('/content/product-slots', methods=['POST'])
@require_auth_and_permissions()
def add_product_slot():
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())
    instance = ProductSlotSchema().load(raw_data)
    db.product_slots.insert_one(instance)
    return '', 204


# TODO both PUT and DELETE methods need another way to check ownership

@doc(tags=['Product Slots'], description='')
@marshal_with(ProductSlotSchema())
@content.route('/content/product-slots/<string:instance_id>', methods=['PUT'])
@require_auth_and_permissions()
# @check_ownership('/content/product-providers', 'owner_id')
def replace_product_slot(instance_id):
    raw_data = request.get_json()
    instance = ProductSlotSchema().load(request.get_json(raw_data))
    result = db.product_slots.replace_one({'_id': ObjectId(instance_id)}, instance)

    if not result.matched_count:
        raw_data['_id'] = ObjectId(instance_id)
        instance = ProductSlotSchema().load(request.get_json(raw_data))
        db.product_slots.insert_one(instance)
        return '', 201

    return '', 204


@doc(tags=['Product Slots'], description='')
@marshal_with(ProductProviderSchema())
@content.route('/content/product-slots/<string:instance_id>', methods=['DELETE'])
@require_auth_and_permissions()
# @check_ownership('/content/product-providers', 'owner_id')
def remove_product_slot(instance_id):
    result = db.product_slots.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200
