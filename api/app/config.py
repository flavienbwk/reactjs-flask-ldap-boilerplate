import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
    POSTGRES_USER = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB = os.environ.get('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        "{}:{}".format(POSTGRES_HOST, POSTGRES_PORT),
        POSTGRES_DB
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)
