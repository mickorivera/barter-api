from http import HTTPStatus

from flask_login import current_user, login_required
from flask_rebar import get_validated_body
from flask_rebar.errors import NotFound

from app.v1.list.models import ListModel


@login_required
def get_lists():
    return ListModel.select().where(ListModel.is_deleted == False)


@login_required
def get_list_item(id):
    try:
        list_item = ListModel.get(id=id, is_deleted=False)
    except ListModel.DoesNotExist:
        raise NotFound
    else:
        return list_item


@login_required
def create_list():
    data = get_validated_body()

    list_item = ListModel.create(author=current_user.id, **data)

    return list_item


@login_required
def update_list_item(id):
    data = get_validated_body()

    updated_items = (
        ListModel.update(**data)
        .where(ListModel.id == id, ListModel.is_deleted == False)
        .execute()
    )

    if not updated_items:
        raise NotFound

    return ListModel.get(id=id, is_deleted=False)


@login_required
def delete_list_item(id):
    ListModel.update(is_deleted=True).where(ListModel.id == id).execute()

    return "", 204
