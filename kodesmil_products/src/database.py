import os
from flask_pymongo import PyMongo


class Database:

    def __init__(self, app):
        app.config["MONGO_URI"] = 'mongodb+srv://{}:{}@{}/{}'.format(
            os.environ['MONGODB_USERNAME'],
            os.environ['MONGODB_PASSWORD'],
            os.environ['MONGODB_HOSTNAME'],
            os.environ['MONGODB_DB_PRODUCTS'],
        )
        mongo = PyMongo(app)
        self.db = mongo.db
