from flask import Blueprint, jsonify, request

from _utils.db import db_conn

from .models import *

from bson.objectid import ObjectId

content = Blueprint('content', __name__)
db = db_conn()


# SERVICES


@content.route('/content/services')
def get_services():
	schema = ServiceSchema(many=True)
	instances = schema.dump(
		db.services.find()
	)
	return jsonify(instances.data)


@content.route('/content/services', methods=['POST'])
def add_service():
	instance = ServiceSchema().load(request.get_json())
	print(instance)
	db.services.insert_one(instance.data)
	return '', 204


# SERVICE CATEGORIES


@content.route('/content/service-categories')
def get_service_categories():
	schema = ServiceCategorySchema(many=True)
	instances = schema.dump(
		db.service_categories.find()
	)
	return jsonify(instances.data)


@content.route('/content/service-categories', methods=['POST'])
def add_service_category():
	instance = ServiceCategorySchema().load(request.get_json())
	db.service_categories.insert_one(instance.data)
	return '', 204


@content.route('/content/service-categories/services')
def get_services_by_category():
	schema = ServiceSchema(many=True)
	instances = schema.dump(
		db.services.find(
			{
				"category": ObjectId(request.json['category_id'])
			}
		)
	)
	return jsonify(instances.data)


# SERVICE PROVIDERS


@content.route('/content/service-providers')
def get_service_providers():
	schema = ServiceProviderSchema(many=True)
	instances = schema.dump(
		db.service_providers.find()
	)
	return jsonify(instances.data)


@content.route('/content/service-providers', methods=['POST'])
def add_service_provider():
	instance = ServiceProviderSchema().load(request.get_json())
	db.service_providers.insert_one(instance.data)
	return '', 204


# SERVICE SLOTS


@content.route('/content/service-slots')
def get_service_slots():
	schema = ServiceSlotSchema(many=True)
	instances = schema.dump(
		db.service_slots.find()
	)
	return jsonify(instances.data)


@content.route('/content/service-slots', methods=['POST'])
def add_service_slot():
	instance = ServiceSlotSchema().load(request.get_json())
	db.service_slots.insert_one(instance.data)
	return '', 204
