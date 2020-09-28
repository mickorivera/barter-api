import os
import pytest

from app.constants import UserRole
from app.v1.card.models import CardModel
from app.v1.comment.models import CommentModel, CommentReplyModel
from app.v1.list.models import ListModel
from app.v1.user.models import UserModel
from app.utils.hashing import get_hash


@pytest.fixture(scope="session", autouse=True)
def users():
    if UserModel.table_exists():
        UserModel.truncate_table(cascade=True)

    UserModel.create_table()

    salt = os.urandom(32)
    users = [
        UserModel.create(
            username="user1",
            email_address="user1@gmail.com",
            key=get_hash(password="password1", salt=salt),
            salt=salt,
            role=UserRole.ADMIN,
        ),
        UserModel.create(
            username="user2",
            email_address="user2@gmail.com",
            key=get_hash(password="password2", salt=salt),
            salt=salt,
            role=UserRole.ADMIN,
        ),
        UserModel.create(
            username="user3",
            email_address="user3@gmail.com",
            key=get_hash(password="password3", salt=salt),
            salt=salt,
        ),
        UserModel.create(
            username="user4",
            email_address="user4@gmail.com",
            key=get_hash(password="password4", salt=salt),
            salt=salt,
        ),
    ]
    yield users

    UserModel.truncate_table(cascade=True)


@pytest.fixture(scope="session", autouse=True)
def admins(users):
    yield [user for user in users if user.role == UserRole.ADMIN]


@pytest.fixture(scope="session", autouse=True)
def members(users):
    yield [user for user in users if user.role == UserRole.MEMBER]


@pytest.fixture(scope="session", autouse=True)
def lists(admins):
    if ListModel.table_exists():
        ListModel.truncate_table(cascade=True)

    lists = []
    for admin in admins:
        for list_index in range(2):
            lists.append(
                ListModel.create(
                    author=admin, title=f"{admin.username} list {list_index}"
                )
            )

    yield lists

    ListModel.truncate_table(cascade=True)
