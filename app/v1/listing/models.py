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
from app.constants import Currency, ItemCondition, ItemStatus
from app.v1.user.models import UserModel


class TagModel(BaseSQLModel):
    id = AutoField()
    value = CharField(unique=True, max_length=64)
    raw_value = CharField(max_length=64)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "tags"

    def __str__(self):
        return self.value

    def get(self, **kwargs):
        kwargs["value"] = kwargs["value"].lower()
        return super().get(**kwargs)

    def save(self, *args, **kwargs):
        self.raw_value = self.value
        self.value = self.value.lower()
        return super().save(*args, **kwargs)


class BrandModel(BaseSQLModel):
    id = AutoField()
    name = CharField(unique=True, max_length=64)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "brands"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


class CategoryModel(BaseSQLModel):
    id = AutoField()
    name = CharField(unique=True, max_length=64)
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)


class ItemModel(BaseSQLModel):
    id = AutoField()
    title = CharField(max_length=64)
    user = ForeignKeyField(UserModel, backref="items", on_delete="CASCADE")
    category = ForeignKeyField(
        CategoryModel, backref="items", on_delete="CASCADE"
    )
    brand = ForeignKeyField(BrandModel, backref="items", on_delete="CASCADE")
    tags = ManyToManyField(TagModel, backref="items")

    condition = CharField(choices=ItemCondition)
    value = DecimalField(decimal_places=2, auto_round=True)
    currency = CharField(choices=Currency)
    description = CharField(max_length=128)
    status = CharField(choices=ItemStatus, default=ItemStatus.AVAILABLE)
    preference_score_rate = DecimalField(
        decimal_places=2, auto_round=True, default=0
    )
    popularity_rate = DecimalField(
        decimal_places=2, auto_round=True, default=0
    )
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "items"

    def __str__(self):
        return self.name


ItemTagModel = ItemModel.tags.get_through_model()


class ImageModel(BaseSQLModel):
    id = AutoField()
    url = CharField(max_length=256)
    item = ForeignKeyField(ItemModel, backref="images", on_delete="CASCADE")
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "images"

    def __str__(self):
        return self.url


class MatchModel(BaseSQLModel):
    id = AutoField()
    item_a = ForeignKeyField(ItemModel, index=True, related_name="matches_a")
    item_b = ForeignKeyField(ItemModel, index=True, related_name="matches_b")
    date_created = DateTimeField(null=True)
    date_updated = DateTimeField(null=True)
    is_deleted = BooleanField(default=False)

    class Meta(BaseSQLModel):
        table_name = "matches"

    def __str__(self):
        return f"{self.item_a} - {self.item_b}"
