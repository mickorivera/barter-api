import logging
import os
import random

from app.constants import Currency, ItemCondition, ItemStatus, UserRole
from app.v1.listing.models import (
    BrandModel,
    CategoryModel,
    ImageModel,
    ItemModel,
    MatchModel,
    TagModel,
)
from app.v1.user.models import UserModel
from app.utils.hashing import get_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clear_table():
    for table_model in (
        UserModel,
        ItemModel,
        MatchModel,
        ImageModel,
        TagModel,
        CategoryModel,
        BrandModel,
    ):
        logger.info(f"Truncating {table_model._meta.table_name} table...")
        table_model.truncate_table(cascade=True)


def seed_users():

    user_data = [
        {
            "username": "micko",
            "password": "micko",
            "salt": os.urandom(32),
            "email_address": "micko@gmail.com",
            "role": UserRole.ADMIN,
        },
        {
            "username": "michael",
            "password": "michael",
            "salt": os.urandom(32),
            "email_address": "michael@gmail.com",
            "role": UserRole.ADMIN,
        },
        {
            "username": "angelo",
            "password": "angelo",
            "salt": os.urandom(32),
            "email_address": "angelo@gmail.com",
        },
        {
            "username": "rivera",
            "password": "rivera",
            "salt": os.urandom(32),
            "email_address": "rivera@gmail.com",
        },
    ]

    for data in user_data:
        user = UserModel.create(
            **data,
            key=get_hash(password=data["password"], salt=data["salt"]),
        )
        logger.info(f"Created {user}")
        yield user


def seed_tags():
    for tag_value in (
        "houseandLot",
        "AutoMobile",
        "Clothing",
        "laptops",
        "Chairs",
    ):
        tag = TagModel.create(value=tag_value)
        logger.info(f"Created {tag}")
        yield tag


def seed_brands():
    for brand_name in "Ayala", "Porsche", "Gucci", "Samsung", "Edra":
        brand = BrandModel.create(name=brand_name)
        logger.info(f"Created {brand}")
        yield brand


def seed_categories():
    for category_name in "property", "car", "fashion", "gadget", "furniture":
        category = CategoryModel.create(name=category_name)
        logger.info(f"Created {category}")
        yield category


def seed_items(users):
    tags = [tag for tag in seed_tags()]
    categories = [cluster for cluster in seed_categories()]
    brands = [brand for brand in seed_brands()]

    for user, tag, category, brand in zip(users, tags, categories, brands):
        item = ItemModel.create(
            title=f"Trading my {brand} {category}!",
            user=user,
            category=category,
            brand=brand,
            condition=random.choice(ItemCondition),
            value=random.uniform(1, 100),
            currency=Currency.PHP,
            description=f"{brand} {category} #{tag}",
            status=random.choice(ItemStatus),
        )

        item.tags.add(tag)
        yield item


if __name__ == "__main__":
    clear_table()
    users = [user for user in seed_users()]
    items = [item for item in seed_items(users)]
