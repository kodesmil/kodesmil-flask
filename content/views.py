from flask import Blueprint, jsonify, request

from pymongo import MongoClient

from .models import *

content = Blueprint('content', __name__)
db_client = MongoClient('localhost', 27017)
db = db_client.kodesmil


@content.route('/content')
def get_services():
	schema = ServiceSchema(many=True)
	services = schema.dump(
		db.services.find()
	)
	return jsonify(services.data)


@content.route('/content', methods=['POST'])
def add_service():
	service = ServiceSchema().load(request.get_json())
	db.services.insert_one(service.data)
	return '', 204

