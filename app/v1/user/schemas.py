from marshmallow import fields, Schema, validate

from app.constants import UserRole


class UserSchema(Schema):
    # TODO: secure password
    # TODO: validate email/username
    id = fields.Integer(dump_only=True)
    email_address = fields.String()
    username = fields.String()
    password = fields.String(load_only=True)
    date_created = fields.String(dump_only=True)
    date_updated = fields.String(dump_only=True)
    role = fields.String(
        default=UserRole.MEMBER, validate=validate.OneOf(UserRole)
    )


class UserLoginSchema(Schema):
    username = fields.String()
    password = fields.String(load_only=True)
