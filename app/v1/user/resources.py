import os

from flask import redirect, url_for
from flask_login import login_required, login_user, logout_user
from flask_rebar import get_validated_body
from flask_rebar.errors import NotFound, Unauthorized

from app.utils.hashing import get_hash
from app.v1.user.models import UserModel


@login_required
def get_user_list():
    return UserModel.select()


def create_user():
    validated_body = get_validated_body()

    salt = os.urandom(32)
    user = UserModel.create(
        username=validated_body.get("username"),
        email_address=validated_body.get("username"),
        salt=salt,
        key=get_hash(password=validated_body.get("password"), salt=salt),
    )

    return user


def login():
    validated_body = get_validated_body()

    try:
        user = UserModel.get(
            username=validated_body.get("username"), is_deleted=False
        )
    except UserModel.DoesNotExist:
        raise NotFound

    if user.key.tobytes() != get_hash(
        password=validated_body.get("password"), salt=user.salt
    ):
        raise Unauthorized

    login_user(user=user)

    return user


@login_required
def logout():
    logout_user()

    return redirect(next or url_for("index"))
