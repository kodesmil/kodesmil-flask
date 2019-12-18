from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
from .views import *
import flask_monitoringdashboard as dashboard
from flask_apispec import FlaskApiSpec

# main file for testing
# simply run this as flask app
# happy debugging! ;)

# app setup

app = Flask(__name__)
app.register_blueprint(content)

# dashboard setup
dashboard.bind(app)

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

docs.register(get_services, endpoint='get_services', blueprint='content')
docs.register(add_service, endpoint='add_service', blueprint='content')
docs.register(filter_services, endpoint='filter_services', blueprint='content')

docs.register(get_service_categories, endpoint='get_service_categories', blueprint='content')
docs.register(add_service_category, endpoint='add_service_category', blueprint='content')

docs.register(get_service_providers, endpoint='get_service_providers', blueprint='content')
docs.register(add_service_provider, endpoint='add_service_provider', blueprint='content')

docs.register(get_service_slots, endpoint='get_service_slots', blueprint='content')
docs.register(add_service_slot, endpoint='add_service_slot', blueprint='content')
