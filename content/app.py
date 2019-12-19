import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask
#import flask_monitoringdashboard as dashboard

from flask_pymongo import PyMongo
import views
# main file for testing
# simply run this as flask app
# happy debugging! ;)

# app setup

app = Flask(__name__)
app.register_blueprint(views.content)

app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + \
    '@' + os.environ['MONGODB_HOSTNAME'] + \
    ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(app)
db = mongo.db


# dashboard setup
# dashboard.bind(app)

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

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
