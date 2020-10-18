# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class BrandModel(peewee.Model):
    name = CharField(max_length=64, unique=True)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "brands"


@snapshot.append
class CategoryModel(peewee.Model):
    name = CharField(max_length=64, unique=True)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "categories"


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
class ItemModel(peewee.Model):
    title = CharField(max_length=64)
    user = snapshot.ForeignKeyField(
        backref="items", index=True, model="usermodel", on_delete="CASCADE"
    )
    category = snapshot.ForeignKeyField(
        backref="items", index=True, model="categorymodel", on_delete="CASCADE"
    )
    brand = snapshot.ForeignKeyField(
        backref="items", index=True, model="brandmodel", on_delete="CASCADE"
    )
    condition = CharField(max_length=255)
    value = DecimalField(
        auto_round=True,
        decimal_places=2,
        max_digits=10,
        rounding="ROUND_HALF_EVEN",
    )
    currency = CharField(max_length=255)
    description = CharField(max_length=128)
    status = CharField(default="AVAILABLE", max_length=255)
    preference_score_rate = DecimalField(
        auto_round=True,
        decimal_places=2,
        default=0,
        max_digits=10,
        rounding="ROUND_HALF_EVEN",
    )
    popularity_rate = DecimalField(
        auto_round=True,
        decimal_places=2,
        default=0,
        max_digits=10,
        rounding="ROUND_HALF_EVEN",
    )
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "items"


@snapshot.append
class ImageModel(peewee.Model):
    url = CharField(max_length=256)
    item = snapshot.ForeignKeyField(
        backref="images", index=True, model="itemmodel", on_delete="CASCADE"
    )
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "images"


@snapshot.append
class TagModel(peewee.Model):
    value = CharField(max_length=64, unique=True)
    raw_value = CharField(max_length=64)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "tags"


@snapshot.append
class ItemModelTagModelThrough(peewee.Model):
    itemmodel = snapshot.ForeignKeyField(index=True, model="itemmodel")
    tagmodel = snapshot.ForeignKeyField(index=True, model="tagmodel")

    class Meta:
        table_name = "items_tags_through"
        indexes = ((("itemmodel", "tagmodel"), True),)


@snapshot.append
class MatchModel(peewee.Model):
    item_a = snapshot.ForeignKeyField(
        backref="matches_a", index=True, model="itemmodel"
    )
    item_b = snapshot.ForeignKeyField(
        backref="matches_b", index=True, model="itemmodel"
    )
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta:
        table_name = "matches"
