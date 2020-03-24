from marshmallow import Schema, fields, validate


# TODO decide which fields are required, and what should be their max size


# PRODUCTS


class ProductSchema(Schema):
    _id = fields.String()
    name = fields.Str(
        required = True,
        validate = validate.Length(min=1),
    )
    price = fields.Float(
        required = True,
    )
    description = fields.Str()
    category = fields.Str(required = True)
    provider = fields.Str(required = True)
    picture = fields.Url()
    slotable = fields.Bool(default = False)
    updated_at = fields.DateTime()


# PRODUCT CATEGORIES


class ProductCategorySchema(Schema):
    _id = fields.Str()
    name = fields.Str(
        required = True,
        validate = validate.Length(min=1),
    )


# PRODUCT PROVIDERS


class ProductProviderSchema(Schema):
    _id = fields.Str()
    name = fields.Str(
        required = True,
        validate = validate.Length(min=1)
    )
    owner_id = fields.Str(required = True)


# PRODUCT SLOTS


class ProductSlotSchema(Schema):
    _id = fields.Str()
    duration = fields.Integer(required = True)
    product = fields.Str(required = True)
    user_id = fields.Str(required = True)
    starting_at = fields.DateTime(required = True)
    updated_at = fields.DateTime()
