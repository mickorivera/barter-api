import inspect
from datetime import datetime

from playhouse.postgres_ext import Model, PostgresqlDatabase

from config import get_config

config = get_config()
postgre_client = PostgresqlDatabase(
    config.POSTGRESQL_DB_NAME,
    host=config.POSTGRESQL_DB_HOST,
    port=config.POSTGRESQL_DB_PORT,
    user=config.POSTGRESQL_DB_USERNAME,
    password=config.POSTGRESQL_DB_PASSWORD,
)


def ensure_connection(func):
    def decorated(cls, *args, **kwargs):
        if cls._meta.database.in_transaction():
            return func(cls, *args, **kwargs)

        cls._meta.database.connect(reuse_if_open=True)
        with cls._meta.database.connection_context():
            returned_value = func(cls, *args, **kwargs)

        return returned_value

    return decorated


class BaseSQLModel(Model):
    """Base model for all PostgreSQL models."""

    class Meta:
        database = postgre_client

    @classmethod
    def _get_utc_timestamp(cls):
        """Returns current time in UTC"""
        return datetime.utcnow()

    @classmethod
    def _raise_attr_error(cls):
        """Generic error to avoid usage of unimplemented db functions"""
        raise AttributeError(
            "'{}' object has no attribute '{}'".format(
                cls.__name__, inspect.currentframe().f_code.co_name
            )
        )

    @classmethod
    @ensure_connection
    def create(cls, **query):
        """Creates record of model class"""
        if "date_created" not in query:
            query["date_created"] = cls._get_utc_timestamp()
            query["date_updated"] = cls._get_utc_timestamp()
        return super().create(**query)

    @ensure_connection
    def insert(self, **insert):
        if "date_updated" not in insert:
            insert["date_updated"] = self._get_utc_timestamp()
        return super(BaseSQLModel, self).insert(**insert)

    @ensure_connection
    def save(self, force_insert=False, only=None):
        return super(BaseSQLModel, self).save(
            force_insert=force_insert, only=only
        )

    @classmethod
    @ensure_connection
    def select(cls, *fields):
        return super().select(*fields)

    @classmethod
    @ensure_connection
    def update(cls, *args, **kwargs):
        if "date_updated" not in kwargs:
            kwargs["date_updated"] = cls._get_utc_timestamp()
        return super().update(*args, **kwargs)

    # restricted db functions
    @classmethod
    def delete(cls):
        cls._raise_attr_error()

    @classmethod
    def bulk_create(cls, model_list, batch_size=None):
        cls._raise_attr_error()

    @classmethod
    def delete_by_id(cls, pk):
        cls._raise_attr_error()

    def delete_instance(self, recursive=False, delete_nullable=False):
        self._raise_attr_error()

    @classmethod
    def insert_from(cls, query, fields):
        cls._raise_attr_error()

    @classmethod
    def insert_many(cls, rows, fields=None):
        cls._raise_attr_error()

    @classmethod
    def replace(cls, __data=None, **insert):
        cls._raise_attr_error()

    @classmethod
    def replace_many(cls, rows, fields=None):
        cls._raise_attr_error()

    @classmethod
    def set_by_id(cls, key, value):
        cls._raise_attr_error()
