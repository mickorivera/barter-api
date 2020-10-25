from flask_login import current_user, login_required
from flask_rebar import get_validated_body
from flask_rebar.errors import NotFound

from app.v1.listing.models import (
    BrandModel,
    CategoryModel,
    ItemModel,
    TagModel,
)
from app.v1.user.models import UserModel


@login_required
def get_brand_list():
    return BrandModel.select()


@login_required
def get_category_list():
    return CategoryModel.select()


@login_required
def get_tag_list():
    return TagModel.select()


@login_required
def get_user_item_list(user_id):
    try:
        user = UserModel.get(id=user_id)
    except UserModel.DoesNotExist:
        raise NotFound(f"User {user_id} does not exist")

    return user.items


@login_required
def get_item_details(id):
    try:
        item = ItemModel.get(id=id)
    except ItemModel.DoesNotExist:
        raise NotFound(f"Item {id} does not exist")

    return item


@login_required
def create_item():
    validated_body = get_validated_body()

    tags = []
    for tag_detail in validated_body.pop("tags"):
        tag, _ = TagModel.get_or_create(value=tag_detail["value"])
        tags.append(tag)

    try:
        category_id = validated_body.pop("category")["id"]
        category = CategoryModel.get(id=category_id)
    except CategoryModel.DoesNotExist:
        raise NotFound(f"Category {category_id} does not exist")

    try:
        brand_id = validated_body.pop("brand")["id"]
        brand = BrandModel.get(id=brand_id)
    except BrandModel.DoesNotExist:
        raise NotFound(f"Brand {brand_id} does not exist")

    item = ItemModel.create(
        user=current_user.id,
        brand=brand.id,
        category=category.id,
        **validated_body,
    )
    item.tags.add(tags)

    return item


@login_required
def update_item(id):
    validated_body = get_validated_body()

    try:
        item = ItemModel.get(id=id)
    except ItemModel.DoesNotExist:
        raise NotFound(f"Item {id} does not exist")

    tags = []
    for tag_detail in validated_body.pop("tags", []):
        tag, _ = TagModel.get_or_create(value=tag_detail["value"])
        tags.append(tag)

    if tags:
        item.tags.clear()
        item.tags.add(tags)

    category_details = validated_body.pop("category", None)
    if category_details:
        try:
            category_id = category_details["id"]
            category = CategoryModel.get(id=category_id)
            validated_body["category"] = category.id
        except CategoryModel.DoesNotExist:
            raise NotFound(f"Category {category_id} does not exist")

    brand_details = validated_body.pop("brand", None)
    if brand_details:
        try:
            brand_id = brand_details["id"]
            brand = BrandModel.get(id=brand_id)
            validated_body["brand"] = brand.id
        except BrandModel.DoesNotExist:
            raise NotFound(f"Brand {brand_id} does not exist")

    ItemModel.update(**validated_body).where(ItemModel.id == item.id).execute()

    return ItemModel.get(id=id)


@login_required
def delete_item(id):
    try:
        item = ItemModel.get(id=id)
    except ItemModel.DoesNotExist:
        raise NotFound(f"Item {id} does not exist")

    item.delete_instance()

    return {}, 204
