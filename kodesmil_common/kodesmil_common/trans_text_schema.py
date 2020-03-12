from marshmallow import Schema, fields


class TransTextSchema(Schema):
    en = fields.Str()
    nb = fields.Str()
