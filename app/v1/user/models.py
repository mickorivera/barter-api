from flask_login import UserMixin
from playhouse.postgres_ext import (
    AutoField,
    BlobField,
    CharField,
)

from app.common.models import BaseSQLModel
from app.constants import UserRole


class UserModel(BaseSQLModel, UserMixin):
    id = AutoField()
    username = CharField(unique=True, index=True, max_length=16)
    email_address = CharField(unique=True, max_length=256)
    salt = BlobField()
    key = BlobField()
    role = CharField(choices=UserRole, default=UserRole.MEMBER)

    class Meta(BaseSQLModel):
        table_name = "users"

    def __str__(self):
        return self.username
