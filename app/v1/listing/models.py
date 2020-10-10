from playhouse.postgres_ext import (
    AutoField,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKeyField,
    ManyToManyField,
)

from app.common.models import BaseSQLModel
from app.constants import ItemStatus
from app.v1.user.models import UserModel


class TagModel(BaseSQLModel):
    id = AutoField()
    value = CharField(max_length=64)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)


class ClusterModel(BaseSQLModel):
    id = AutoField()
    name = CharField(max_length=64)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)


class ItemModel(BaseSQLModel):
    id = AutoField()
    user = ForeignKeyField(UserModel, backref="items", on_delete="CASCADE")
    brand = CharField(max_length=64)
    value = DecimalField(decimal_places=2, auto_round=True)
    type = CharField(max_length=64)
    tag = ManyToManyField(TagModel, backref="items")
    description = CharField(max_length=128)
    status = CharField(choices=ItemStatus, default=ItemStatus.AVAILABLE)
    cluster = ForeignKeyField(
        ClusterModel, backref="items", on_delete="CASCADE"
    )
    preference_score_rate = DecimalField(decimal_places=2, auto_round=True)
    popularity_rate = DecimalField(decimal_places=2, auto_round=True)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "items"


class ItemImageModel(BaseSQLModel):
    id = AutoField()
    url = CharField(max_length=256)
    item = ForeignKeyField(
        ItemModel, backref="item_images", on_delete="CASCADE"
    )
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)


class MatchModel(BaseSQLModel):
    item_a = ForeignKeyField(ItemModel, index=True, related_name="matches_a")
    item_b = ForeignKeyField(ItemModel, index=True, related_name="matches_b")
    user_a = ForeignKeyField(ItemModel, index=True, related_name="matches_a")
    user_b = ForeignKeyField(ItemModel, index=True, related_name="matches_b")
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)
