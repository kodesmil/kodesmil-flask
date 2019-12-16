import datetime as dt
import uuid

from marshmallow import Schema, fields


class SampleModel:
	def __init__(self, name, description, category, provider, picture):
		self.id = uuid.uuid4()
		self.created_at = dt.datetime.now()
		self.updated_at = dt.datetime.now()

	def __repr__(self):
		return '<Service(name={self.name!r})>'.format(self=self)


class SampleModelSchema(Schema):
	id = fields.UUID()
	created_at = fields.Date()
	updated_at = fields.Date()
