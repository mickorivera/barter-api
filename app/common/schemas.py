from marshmallow import fields, Schema


class ErrorSchema(Schema):
    message = fields.String()
