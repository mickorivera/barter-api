from playhouse.postgres_ext import (
    AutoField,
    BooleanField,
    CharField,
    ForeignKeyField,
    DateTimeField,
)

from app.common.models import BaseSQLModel
from app.v1.card.models import CardModel
from app.v1.user.models import UserModel


class CommentModel(BaseSQLModel):
    id = AutoField()
    author = ForeignKeyField(
        UserModel, backref="comments", on_delete="CASCADE"
    )
    card = ForeignKeyField(CardModel, backref="comments", on_delete="CASCADE")
    content = CharField(max_length=256)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "comments"


class CommentReplyModel(BaseSQLModel):
    id = AutoField()
    author = ForeignKeyField(UserModel, backref="replies", on_delete="CASCADE")
    comment = ForeignKeyField(
        CommentModel, backref="replies", on_delete="CASCADE"
    )
    content = CharField(max_length=256)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)

    class Meta(BaseSQLModel):
        table_name = "comment_replies"
