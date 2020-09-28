from playhouse.postgres_ext import (
    AutoField,
    BooleanField,
    CharField,
    ForeignKeyField,
    DateTimeField,
)

from app.common.models import BaseSQLModel
from app.v1.list.models import ListModel
from app.v1.user.models import UserModel


class CardModel(BaseSQLModel):
    id = AutoField()
    author = ForeignKeyField(UserModel, backref="cards", on_delete="CASCADE")
    list = ForeignKeyField(ListModel, backref="cards", on_delete="CASCADE")
    title = CharField(max_length=256)
    description = CharField(max_length=1024)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "cards"
