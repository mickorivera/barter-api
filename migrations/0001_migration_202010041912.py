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
