import datetime as dt
import uuid

from marshmallow import Schema, fields


class Service:
	def __init__(self, name, description, category, provider, picture):
		self.id = uuid.uuid4()
		self.name = name
		self.description = description
		self.category = category
		self.provider = provider
		self.picture = picture
		self.created_at = dt.datetime.now()
		self.updated_at = dt.datetime.now()

	def __repr__(self):
		return '<Service(name={self.name!r})>'.format(self=self)


class ServiceSchema(Schema):
	id = fields.UUID()
	name = fields.Str()
	description = fields.Str()
	category = fields.UUID()
	provider = fields.UUID()
	picture = fields.Url()
	created_at = fields.Date()
	updated_at = fields.Date()


class ServiceCategory():
	def __init__(self, name):
		self.id = uuid.uuid4()
		self.name = name

	def __repr__(self):
		return '<ServiceCategory(name={self.name!r})>'.format(self=self)


class ServiceCategorySchema(Schema):
	id = fields.UUID()
	name = fields.Str()


class ServiceProvider():
	def __init__(self, name, owner_id):
		self.id = uuid.uuid4()
		self.name = name
		self.owner_id = owner_id

	def __repr__(self):
		return '<ServiceProvider(name={self.name!r})>'.format(self=self)


class ServiceProviderSchema(Schema):
	id = fields.UUID()
	name = fields.Str()
	owner_id = fields.UUID()


class ServiceSlot():
	def __init__(self, duration, service, starting_at):
		self.id = uuid.uuid4()
		self.duration = duration
		self.service = service
		self.starting_at = starting_at
		self.created_at = dt.datetime.now()
		self.updated_at = dt.datetime.now()

	def __repr__(self):
		return '<ServiceSlot(id={self.id!r})>'.format(self=self)


class ServiceSlotSchema(Schema):
	id = fields.UUID()
	duration = fields.Integer()
	service = fields.UUID()
	starting_at = fields.Date()
	created_at = fields.Date()
	updated_at = fields.Date()
