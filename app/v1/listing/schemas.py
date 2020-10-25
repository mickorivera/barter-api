from flask_marshmallow.fields import URLFor
from marshmallow import fields, Schema, validate

from app.common.fields import DictHyperlinks
from app.constants import Currency, ItemCondition, ItemStatus
from app.v1.user.schemas import UserSchema


class TagSchema(Schema):
    id = fields.Integer(required=True)
    value = fields.String(required=True, load_only=True)
    raw_value = fields.Str(dump_only=True)


class BrandSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)


class CategorySchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)


class ItemSchema(Schema):
    id = fields.Integer(dump_only=True)

    title = fields.String(required=True)
    user = fields.Nested(UserSchema, dump_only=True, only="id")
    category = fields.Nested(CategorySchema, required=True)
    brand = fields.Nested(BrandSchema, required=True)
    tags = fields.Nested(TagSchema, many=True)

    condition = fields.String(
        required=True, validate=validate.OneOf(ItemCondition)
    )
    value = fields.Float(required=True)
    currency = fields.String(required=True, validate=validate.OneOf(Currency))
    description = fields.String(required=True)
    status = fields.String(required=True, validate=validate.OneOf(ItemStatus))
    date_created = fields.String(dump_only=True)
    date_updated = fields.String(dump_only=True)

    _links = DictHyperlinks(
        {
            "self": URLFor("v1.get_item_details", values=dict(id="<id>")),
            "user": URLFor("v1.get_user_details", values=dict(id="<user_id>")),
            "user_items": URLFor(
                "v1.get_user_item_list", values=dict(user_id="<user_id>")
            ),
        },
        dump_only=True,
    )
