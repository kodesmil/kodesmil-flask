from flask import Blueprint, jsonify, request
from bson.objectid import ObjectId
import datetime as dt
from flask_apispec import marshal_with, doc
from marshmallow import ValidationError
from kodesmil_common.auth import requires_auth

from .models import *
from . import db

products = Blueprint('products', __name__)

product_id_fields = [
    '_id',
    'category',
    'provider'
]


# PRODUCTS

# returns every Product instances in DB

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema(many=True))
@products.route('/products/products', methods=['GET'])
@requires_auth
def get_products():
    schema = ProductSchema(many=True)
    instances = schema.dump(
        db.products.find()
    )
    return jsonify(instances)


# return only one instance of data

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema(many=True))
@products.route('/products/products/<string:instance_id>', methods=['GET'])
@requires_auth
def get_product(user_id, instance_id):
    schema = ProductSchema()

    instance = schema.dump(
        db.products.find_one({'_id': ObjectId(instance_id)})
    )

    return jsonify(instance)


# creates an instance

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema())
@products.route('/products/products', methods=['POST'])
@requires_auth
def add_product(user_id):
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())

    try:
        instance = ProductSchema().load(request.get_json(raw_data))
        result = db.products.insert_one(instance)
        return str(result.inserted_id), 201
    except ValidationError as err:
        return err.messages, 400


# replaces an instance with recieved data
# but, only if user is owner of this instance
#@TODO test it well!

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema())
@products.route('/products/products/<string:instance_id>', methods=['PUT'])
@requires_auth
#@check_ownership('/products/products', 'provider')
def replace_product(user_id, instance_id):
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())

    try:
        instance = ProductSchema().load(request.get_json(raw_data))
    except ValidationError as err:
        return err.messages, 400
    else:
        result = db.products.replace_one({'_id': ObjectId(instance_id)}, instance)

        if not result.matched_count:
            raw_data['_id'] = ObjectId(instance_id)
            try:
                instance = ProductSchema().load(request.get_json(raw_data))
                response = db.products.insert_one(instance)
                return str(response.inserted_id), 201
            except ValidationError as err:
                return err.messages, 400


    return '', 204


# removes product instance

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema())
@products.route('/products/products/<string:instance_id>', methods=['DELETE'])
@requires_auth
#@check_ownership('/products/products', 'provider')
def remove_product(user_id, instance_id):
    result = db.products.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200


# filter Products by anything you like, eg. id, category, provider etc.

@doc(tags=['Products'], description='')
@marshal_with(ProductSchema(many=True))
@products.route('/products/products/filter')
@requires_auth
def filter_products(user_id):
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
@products.route('/products/product-categories', methods=['GET'])
@requires_auth
def get_product_categories(user_id):
    schema = ProductCategorySchema(many=True)
    instances = schema.dump(
        db.product_categories.find()
    )
    return jsonify(instances)


# PRODUCT PROVIDERS

@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema(many=True))
@products.route('/products/product-providers', methods=['GET'])
@requires_auth
def get_product_providers(user_id):
    schema = ProductProviderSchema(many=True)
    instances = schema.dump(
        db.product_providers.find()
    )
    return jsonify(instances)


@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema())
@products.route('/products/product-providers/<string:instance_id>', methods=['GET'])
@requires_auth
def get_product_provider(user_id, instance_id):
    schema = ProductProviderSchema()
    instance = schema.dump(
        db.product_providers.find_one({'_id': ObjectId(instance_id)})
    )
    return jsonify(instance)


@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema())
@products.route('/products/product-providers', methods=['POST'])
@requires_auth
def add_product_provider(user_id):

    try:
        instance = ProductProviderSchema().load(request.get_json())
        response = db.product_providers.insert_one(instance)
        return str(response.inserted_id), 201
    except ValidationError as err:
        return err.messages, 400

#@TODO test it

@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema())
@products.route('/products/product-providers/<string:instance_id>', methods=['PUT'])
@requires_auth
#@check_ownership('/products/product-providers', 'owner_id')
def replace_product_provider(user_id, instance_id):
    raw_data = request.get_json()

    try:
        instance = ProductProviderSchema().load(request.get_json(raw_data))
    except ValidationError as err:
        return err.messages, 400
    else:
        result = db.product_providers.replace_one({'_id': ObjectId(instance_id)}, instance)
        if not result.matched_count:
            raw_data['_id'] = ObjectId(instance_id)
            try:
                instance = ProductProviderSchema().load(request.get_json(raw_data))
            except ValidationError as err:
                return err.messages, 400
            response = db.product_providers.insert_one(instance)
            return str(response.inserted_id), 201
    return '', 204


@doc(tags=['Product Providers'], description='')
@marshal_with(ProductProviderSchema())
@products.route('/products/product-providers/<string:instance_id>', methods=['DELETE'])
@requires_auth
#@check_ownership('/products/product-providers', 'owner_id')
def remove_product_provider(user_id, instance_id):
    result = db.product_providers.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200


# PRODUCT SLOTS


@doc(tags=['Product Slots'], description='')
@marshal_with(ProductSlotSchema(many=True))
@products.route('/products/product-slots', methods=['GET'])
@requires_auth
def get_product_slots(user_id):
    schema = ProductSlotSchema(many=True)
    instances = schema.dump(
        db.product_slots.find()
    )
    return jsonify(instances)


@doc(tags=['Product Slots'], description='')
@marshal_with(ProductSlotSchema())
@products.route('/products/product-slots/<string:instance_id>', methods=['GET'])
@requires_auth
def get_product_slot(user_id, instance_id):
    schema = ProductSlotSchema()
    instance = schema.dump(
        db.product_slots.find_one({'_id': ObjectId(instance_id)})
    )
    return jsonify(instance)


@doc(tags=['Product Slots'], description='')
@marshal_with(ProductSlotSchema())
@products.route('/products/product-slots', methods=['POST'])
@requires_auth
def add_product_slot(user_id):
    raw_data = request.get_json()
    raw_data['updated_at'] = str(dt.datetime.now(dt.timezone.utc).isoformat())

    try:
        instance = ProductSlotSchema().load(raw_data)
        result =db.product_slots.insert_one(instance)
        return str(result.inserted_id), 201
    except ValidationError as err:
        return err.messages, 400


# TODO both PUT and DELETE methods need another way to check ownership

@doc(tags=['Product Slots'], description='')
@marshal_with(ProductSlotSchema())
@products.route('/products/product-slots/<string:instance_id>', methods=['PUT'])
@requires_auth
# @check_ownership('/products/product-providers', 'owner_id')
def replace_product_slot(user_id, instance_id):
    raw_data = request.get_json()

    try:
        instance = ProductSlotSchema().load(request.get_json(raw_data))
    except ValidationError as err:
        return err.messages, 400

    else:
        result = db.product_slots.replace_one({'_id': ObjectId(instance_id)}, instance)

        if not result.matched_count:
            raw_data['_id'] = ObjectId(instance_id)

            try:
                instance = ProductSlotSchema().load(request.get_json(raw_data))
            except ValidationError as err:
                return err.messages, 400

            result = db.product_slots.insert_one(instance)
            return result.inserted_id, 201


@doc(tags=['Product Slots'], description='')
@marshal_with(ProductProviderSchema())
@products.route('/products/product-slots/<string:instance_id>', methods=['DELETE'])
@requires_auth
# @check_ownership('/products/product-providers', 'owner_id')
def remove_product_slot(user_id, instance_id):
    result = db.product_slots.delete_one({
        '_id': ObjectId(instance_id)
    })
    if not result.matched_count:
        return '', 204
    return '', 200
