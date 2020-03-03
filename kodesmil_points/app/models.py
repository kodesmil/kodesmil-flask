from marshmallow import Schema, fields


class ActivityPointsSchema(Schema):
    _id = fields.Str()
    user_id = fields.Str()
    value = fields.Integer()
    activity_id = fields.Str()
