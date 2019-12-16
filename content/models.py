import datetime as dt
import uuid

from marshmallow import Schema, fields


# SERVICE


class Service:
	def __init__(self, name, description, category, provider, picture):
		self.name = name
		self.description = description
		self.category = category
		self.provider = provider
		self.picture = picture
		self.updated_at = dt.datetime.now()

	def __repr__(self):
		return '<Service(name={self.name!r})>'.format(self=self)


class ServiceSchema(Schema):
	_id = fields.String()
	name = fields.Str()
	description = fields.Str()
	category = fields.Str()
	provider = fields.Str()
	picture = fields.Url()
	updated_at = fields.Date()


# SERVICE CATEGORIES


class ServiceCategory:
	def __init__(self, name):
		self.id = uuid.uuid4()
		self.name = name

	def __repr__(self):
		return '<ServiceCategory(name={self.name!r})>'.format(self=self)


class ServiceCategorySchema(Schema):
	_id = fields.Str()
	name = fields.Str()


# SERVICE PROVIDERS

class ServiceProvider:
	def __init__(self, name, owner_id):
		self.name = name
		self.owner_id = owner_id

	def __repr__(self):
		return '<ServiceProvider(name={self.name!r})>'.format(self=self)


class ServiceProviderSchema(Schema):
	_id = fields.Str()
	name = fields.Str()
	owner_id = fields.Str()


# SERVICE SLOTS


class ServiceSlot:
	def __init__(self, duration, service, starting_at):
		self.duration = duration
		self.service = service
		self.starting_at = starting_at
		self.updated_at = dt.datetime.now()

	def __repr__(self):
		return '<ServiceSlot(id={self.id!r})>'.format(self=self)


class ServiceSlotSchema(Schema):
	_id = fields.Str()
	duration = fields.Integer()
	service = fields.Str()
	starting_at = fields.Date()
	updated_at = fields.Date()
