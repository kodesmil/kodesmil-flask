import os

from bson import ObjectId
from flask_pymongo import PyMongo
from marshmallow import Schema, fields


class Database:

    def __init__(self, app):
        Schema.TYPE_MAPPING[ObjectId] = fields.String
        app.config["MONGO_URI"] = 'mongodb+srv://{}:{}@{}/{}?retryWrites=true&w=majority'.format(
            os.environ['MONGODB_USERNAME'],
            os.environ['MONGODB_PASSWORD'],
            os.environ['MONGODB_HOSTNAME'],
            os.environ['MONGODB_DATABASE'],
        )
        mongo = PyMongo(app)
        self.db = mongo.db
