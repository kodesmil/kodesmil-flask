import os

from flask import Flask
#import flask_monitoringdashboard as dashboard

from flask_pymongo import PyMongo
import views
import docs

app = Flask(__name__)
app.register_blueprint(views.content)

app.config["MONGO_URI"] = 'mongodb://{}:{}@{}:27017/{}'.format(
    os.environ['MONGODB_USERNAME'],
    os.environ['MONGODB_PASSWORD'],
    os.environ['MONGODB_HOSTNAME'],
    os.environ['MONGODB_DATABASE'],
)
mongo = PyMongo(app)
db = mongo.db

# dashboard setup
# dashboard.bind(app)

documentation = docs.Documentation(app)
documentation.initialize()

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
