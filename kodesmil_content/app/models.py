from marshmallow import Schema, fields


# TODO decide which fields are required, and what should be their max size


# PRODUCTS


class ProductSchema(Schema):
    _id = fields.String()
    name = fields.Str()
    description = fields.Str()
    category = fields.Str()
    provider = fields.Str()
    picture = fields.Url()
    updated_at = fields.DateTime()


# PRODUCT CATEGORIES


class ProductCategorySchema(Schema):
    _id = fields.Str()
    name = fields.Str()


# PRODUCT PROVIDERS


class ProductProviderSchema(Schema):
    _id = fields.Str()
    name = fields.Str()
    owner_id = fields.Str()


# PRODUCT SLOTS


class ProductSlotSchema(Schema):
    _id = fields.Str()
    duration = fields.Integer()
    product = fields.Str()
    starting_at = fields.DateTime()
    updated_at = fields.DateTime()
