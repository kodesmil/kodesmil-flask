from marshmallow import Schema, fields

from kodesmil_common.object_id import ObjectId


class ActivitySchema(Schema):
    _id = ObjectId()
    _user_id = ObjectId()
    value = fields.Float()
    registered_from = fields.DateTime()
    registered_to = fields.DateTime()
    source = fields.Str()
    type = fields.Str()
