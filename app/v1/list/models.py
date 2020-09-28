from playhouse.postgres_ext import (
    AutoField,
    BooleanField,
    CharField,
    ForeignKeyField,
    DateTimeField,
)

from app.common.models import BaseSQLModel
from app.v1.user.models import UserModel


class ListModel(BaseSQLModel):
    id = AutoField()
    # TODO: Restrict author must be role ADMIN
    author = ForeignKeyField(UserModel, backref="lists", on_delete="CASCADE")
    title = CharField(max_length=256)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "lists"
