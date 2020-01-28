from marshmallow import Schema, fields
from marshmallow_enum import EnumField
from enum import Enum


class Source(Enum):
    google_fit = 1
    health_kit = 2
    garmin = 3


class Type(Enum):
    steps = 1
    distance = 2


class ActivitySchema(Schema):
    _id = fields.String()
    user_id = fields.Str()
    value = fields.Integer()
    registered_from = fields.DateTime()
    registered_to = fields.DateTime()
    source = EnumField(Source)
    type= EnumField(Type)