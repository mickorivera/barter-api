from app.v1.listing.models import ItemModel
from app.v1.user.models import UserModel


def get_user_item_list(user_id):
    items = UserModel.get(id=user_id).items

    return items


def get_item_details(id):
    return ItemModel.get(id=id)
