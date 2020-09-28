# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class UserModel(peewee.Model):
    username = CharField(index=True, max_length=16, unique=True)
    email_address = CharField(max_length=256, unique=True)
    salt = BlobField()
    key = BlobField()
    role = CharField(default="MEMBER", max_length=255)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "users"


@snapshot.append
class ListModel(peewee.Model):
    author = snapshot.ForeignKeyField(
        backref="lists", index=True, model="usermodel", on_delete="CASCADE"
    )
    title = CharField(max_length=256)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "lists"


@snapshot.append
class CardModel(peewee.Model):
    author = snapshot.ForeignKeyField(
        backref="cards", index=True, model="usermodel", on_delete="CASCADE"
    )
    list = snapshot.ForeignKeyField(
        backref="cards", index=True, model="listmodel", on_delete="CASCADE"
    )
    title = CharField(max_length=256)
    description = CharField(max_length=1024)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "cards"


@snapshot.append
class CommentModel(peewee.Model):
    author = snapshot.ForeignKeyField(
        backref="comments", index=True, model="usermodel", on_delete="CASCADE"
    )
    card = snapshot.ForeignKeyField(
        backref="comments", index=True, model="cardmodel", on_delete="CASCADE"
    )
    content = CharField(max_length=256)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "comments"


@snapshot.append
class CommentReplyModel(peewee.Model):
    author = snapshot.ForeignKeyField(
        backref="replies", index=True, model="usermodel", on_delete="CASCADE"
    )
    comment = snapshot.ForeignKeyField(
        backref="replies",
        index=True,
        model="commentmodel",
        on_delete="CASCADE",
    )
    content = CharField(max_length=256)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)

    class Meta:
        table_name = "comment_replies"


def forward(old_orm, new_orm):
    usermodel = new_orm["usermodel"]
    listmodel = new_orm["listmodel"]
    cardmodel = new_orm["cardmodel"]
    commentmodel = new_orm["commentmodel"]
    return [
        # Apply default value False to the field usermodel.is_deleted
        usermodel.update({usermodel.is_deleted: False}).where(
            usermodel.is_deleted.is_null(True)
        ),
        # Apply default value False to the field listmodel.is_deleted
        listmodel.update({listmodel.is_deleted: False}).where(
            listmodel.is_deleted.is_null(True)
        ),
        # Apply default value False to the field cardmodel.is_deleted
        cardmodel.update({cardmodel.is_deleted: False}).where(
            cardmodel.is_deleted.is_null(True)
        ),
        # Apply default value False to the field commentmodel.is_deleted
        commentmodel.update({commentmodel.is_deleted: False}).where(
            commentmodel.is_deleted.is_null(True)
        ),
    ]
