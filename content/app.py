import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
#import flask_monitoringdashboard as dashboard
from flask_apispec import FlaskApiSpec

from flask_pymongo import PyMongo

# main file for testing
# simply run this as flask app
# happy debugging! ;)

# app setup
import views

app = Flask(__name__)
app.register_blueprint(views.content)

app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(app)
db = mongo.db


# dashboard setup
#dashboard.bind(app)

# docs setup

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='KodeSmil Flask',
        version='v1',
        openapi_version="3.0.2",
        info=dict(description="KodeSmil microservices API"),
        plugins=[MarshmallowPlugin()],
    ),
    'APISPEC_SWAGGER_UI_URL': '/docs/',
})

docs = FlaskApiSpec(app)

docs.register(views.get_services, endpoint='get_services', blueprint='content')
docs.register(views.add_service, endpoint='add_service', blueprint='content')
docs.register(views.filter_services, endpoint='filter_services', blueprint='content')

docs.register(views.get_service_categories, endpoint='get_service_categories', blueprint='content')
docs.register(views.add_service_category, endpoint='add_service_category', blueprint='content')

docs.register(views.get_service_providers, endpoint='get_service_providers', blueprint='content')
docs.register(views.add_service_provider, endpoint='add_service_provider', blueprint='content')

docs.register(views.get_service_slots, endpoint='get_service_slots', blueprint='content')
docs.register(views.add_service_slot, endpoint='add_service_slot', blueprint='content')


if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
