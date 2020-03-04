from marshmallow import Schema, fields


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
    _id = fields.Str()
    user_id = fields.Str()
    email = fields.Str()
    value = fields.Float()
    registered_from = fields.DateTime()
    registered_to = fields.DateTime()
    source = fields.Str()
    type = fields.Str()
