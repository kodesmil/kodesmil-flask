import bson
from marshmallow import Schema, fields, missing, ValidationError


class ObjectId(fields.Field):

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            return bson.ObjectId(value)
        except:
            raise ValidationError('invalid ObjectId `%s`' % value)

    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return missing
        return str(value)

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


class UserSchema(Schema):
    _id = ObjectId()
    auth_user_id = fields.Str()
    email = fields.Str()
    last_synced_at = fields.DateTime()


class ActivitySchema(Schema):
    _id = ObjectId()
    _user_id = ObjectId()
    value = fields.Float()
    registered_from = fields.DateTime()
    registered_to = fields.DateTime()
    source = fields.Str()
    type = fields.Str()

