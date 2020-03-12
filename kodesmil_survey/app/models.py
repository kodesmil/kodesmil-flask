from marshmallow import Schema, fields

from kodesmil_common.object_id import ObjectId

from kodesmil_common.trans_text_schema import TransTextSchema


class QuestionType:
    rank = 'rank'
    open = 'open'


class QuestionSchema(Schema):
    _id = ObjectId()
    text = fields.Nested(TransTextSchema)
    type = fields.Str()


class AnswerSchema(Schema):
    _id = ObjectId()
    author_id = ObjectId()
    question_id = ObjectId()
    value = fields.Float()
    type = fields.Str()
