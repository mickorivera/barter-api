import os


class Config:
    """Common configurations for the project modules."""

    DEBUG = True
    TEST = False

    POSTGRESQL_DB_NAME = os.getenv("POSTGRESQL_DB_NAME")
    POSTGRESQL_DB_HOST = os.getenv("POSTGRESQL_DB_HOST")
    POSTGRESQL_DB_PORT = os.getenv("POSTGRESQL_DB_PORT")
    POSTGRESQL_DB_USERNAME = os.getenv("POSTGRESQL_DB_USERNAME")
    POSTGRESQL_DB_PASSWORD = os.getenv("POSTGRESQL_DB_PASSWORD")

    API_SECRET_KEY = os.getenv("API_SECRET_KEY")


class LocalConfig:
    """Configuration for debugging purposes."""

    DEBUG = True
    TEST = False

    POSTGRESQL_DB_NAME = "irithm"
    POSTGRESQL_DB_HOST = "127.0.0.1"
    POSTGRESQL_DB_PORT = "5432"
    POSTGRESQL_DB_USERNAME = "postgres"
    POSTGRESQL_DB_PASSWORD = "password"

    API_SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'


class TestConfig(LocalConfig):
    """Configuration for unit testing purposes"""

    TEST = True


class DevelopmentConfig(Config):
    """Development configurations"""

    DEBUG = True


class StagingConfig(Config):
    """Staging configurations"""

    DEBUG = False


class ProductionConfig(Config):
    """Production ready configurations"""

    DEBUG = False


def get_config(config_name=None):
    if not config_name:
        config_name = os.getenv("APP_ENV", "default")

    return {
        "local": LocalConfig,
        "test": TestConfig,
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
        "default": LocalConfig,
    }.get(config_name, LocalConfig)
