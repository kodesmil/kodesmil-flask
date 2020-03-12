from marshmallow import Schema, fields

from kodesmil_common.object_id import ObjectId


class LocationSchema(Schema):
    _id = ObjectId()
    created_at = fields.DateTime()
    user_id = ObjectId()
    lat = fields.Float()
    lon = fields.Float()
    accuracy = fields.Float()
