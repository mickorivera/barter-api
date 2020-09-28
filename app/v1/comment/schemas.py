from marshmallow import fields, Schema


class CommentSchema(Schema):
    content = fields.String()
    author = fields.Integer()


class CommentReplySchema(Schema):
    content = fields.String()
    author = fields.String()
