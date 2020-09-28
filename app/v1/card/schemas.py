from marshmallow import fields, Schema


class CardSchema(Schema):
    title = fields.String()
    description = fields.String()
    author = fields.String()
