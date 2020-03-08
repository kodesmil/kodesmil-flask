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


class SurveyType:
    mood = 'mood'
    health = 'health'


class UserSchema(Schema):
    _id = ObjectId()
    auth_user_id = fields.Str()
    email = fields.Str()
    last_synced_at = fields.DateTime()


class SurveyRankSchema(Schema):
    _id = ObjectId()
    _user_id = ObjectId()
    value = fields.Decimal()
    type = fields.Str()
