# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class UserModel(peewee.Model):
    username = CharField(index=True, max_length=16, unique=True)
    email_address = CharField(max_length=256, unique=True)
    password = CharField(max_length=1024)
    role = CharField(default="MEMBER", max_length=255)
    date_updated = DateTimeField(null=True)

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
