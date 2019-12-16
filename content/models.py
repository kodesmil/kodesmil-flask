import datetime as dt
import uuid

from marshmallow import Schema, fields

# TODO decide which fields are required, and what should be their max size


# SERVICE


class ServiceSchema(Schema):
	_id = fields.String()
	name = fields.Str()
	description = fields.Str()
	category = fields.Str()
	provider = fields.Str()
	picture = fields.Url()
	updated_at = fields.Date()


# SERVICE CATEGORIES


class ServiceCategorySchema(Schema):
	_id = fields.Str()
	name = fields.Str()


# SERVICE PROVIDERS


class ServiceProviderSchema(Schema):
	_id = fields.Str()
	name = fields.Str()
	owner_id = fields.Str()


# SERVICE SLOTS


class ServiceSlotSchema(Schema):
	_id = fields.Str()
	duration = fields.Integer()
	service = fields.Str()
	starting_at = fields.Date()
	updated_at = fields.Date()
