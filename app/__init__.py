import logging
import logging.config
import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_rebar import Rebar
from playhouse.postgres_ext import PostgresqlDatabase

from app.utils.callbacks import raise_unauthorized
from app.v1 import version_1_registry
from config import get_config


class RestApp(Flask):
    def __init__(self):
        super().__init__(__name__)

        # TODO: apply proper CORS values
        CORS(self)
        config = get_config()
        self.config.from_object(config)
        self.url_map.strict_slashes = False
        self.app_context().push()

        self.rebar = Rebar()
        self.rebar.add_handler_registry(version_1_registry)
        self.rebar.init_app(app=self)

        self.secret_key = config.API_SECRET_KEY
        self.login_manager = LoginManager()
        self.login_manager.init_app(app=self)
        self.login_manager.unauthorized_callback = raise_unauthorized

        self._init_logger()
        self._init_db_client()

        self.login_manager.user_loader

    def _init_logger(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        logging.config.fileConfig(f"{base_dir}/logging.conf")

        self.custom_logger = logging.getLogger("irithm")
        self.custom_logger.setLevel(
            logging.DEBUG if self.config["DEBUG"] else logging.INFO
        )

    def _init_db_client(self):
        supported_models = ()

        sql_db_name = self.config["POSTGRESQL_DB_NAME"]
        sql_host = self.config["POSTGRESQL_DB_HOST"]
        sql_username = self.config["POSTGRESQL_DB_USERNAME"]
        self.custom_logger.info(
            f"Binding models to PSQL DB {sql_db_name} from "
            f"{sql_username}@{sql_host}..."
        )
        self.postgre_client = PostgresqlDatabase(
            sql_db_name,
            host=sql_host,
            port=self.config["POSTGRESQL_DB_PORT"],
            user=sql_username,
            password=self.config["POSTGRESQL_DB_PASSWORD"],
        )

        self.postgre_client.bind(
            supported_models, bind_refs=False, bind_backrefs=False
        )
