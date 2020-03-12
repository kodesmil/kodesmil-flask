from marshmallow import Schema, fields

from kodesmil_common.object_id import ObjectId


class Source:
    google_fit = 'google_fit'
    health_kit = 'health_kit'
    garmin = 'garmin'


class Type:
    activity = 'activity'
    steps = 'steps'
    active_minute = 'active_minute'
    distance = 'distance'
    heart_minute = 'heart_minute'


class ActivitySchema(Schema):
    _id = ObjectId()
    _user_id = ObjectId()
    value = fields.Float()
    registered_from = fields.DateTime()
    registered_to = fields.DateTime()
    source = fields.Str()
    type = fields.Str()
