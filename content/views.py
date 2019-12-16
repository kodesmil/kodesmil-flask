from flask import Blueprint, jsonify, request

from .models import *

content = Blueprint('content', __name__)


@content.route('/incomes')
def get_services():
	schema = ServiceSchema(many=True)
	services = schema.dump(
		# get services from db
	)
	return jsonify(services.data)


@content.route('/incomes', methods=['POST'])
def add_service():
	income = ServiceSchema().load(request.get_json())
	# add to DB by PyMongo
	# transactions.append(income.data)

