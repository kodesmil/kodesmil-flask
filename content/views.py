from flask import Blueprint, jsonify, request

from _utils.db import db_conn

from .models import *

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
	db.services.insert_one(instance.data)
	return '', 204


# SERVICE CATEGORIES


@content.route('/content/service-categories')
def get_services():
	schema = ServiceCategorySchema(many=True)
	instances = schema.dump(
		db.services.find()
	)
	return jsonify(instances.data)


@content.route('/content/service-categories', methods=['POST'])
def add_service():
	instance = ServiceProviderSchema().load(request.get_json())
	db.services.insert_one(instance.data)
	return '', 204


# SERVICE PROVIDERS


@content.route('/content/service-providers')
def get_services():
	schema = ServiceProviderSchema(many=True)
	instances = schema.dump(
		db.service_providers.find()
	)
	return jsonify(instances.data)


@content.route('/content/service-providers', methods=['POST'])
def add_service():
	instance = ServiceProviderSchema().load(request.get_json())
	db.service_providers.insert_one(instance.data)
	return '', 204


# SERVICE SLOTS


@content.route('/content/service-slots')
def get_services():
	schema = ServiceSlotSchema(many=True)
	instances = schema.dump(
		db.service_slots.find()
	)
	return jsonify(instances.data)


@content.route('/content/service-slots', methods=['POST'])
def add_service():
	instance = ServiceSlotSchema().load(request.get_json())
	db.service_slots.insert_one(instance.data)
	return '', 204
