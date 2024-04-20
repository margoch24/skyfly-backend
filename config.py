import os

from dotenv import load_dotenv

load_dotenv()


class DefaultConfig:
    PORT = os.environ["PORT"]
    ENV = os.environ["ENV"]
    DATABASE_URI = os.environ["DATABASE_URI"]
    TEST_DATABASE_URI = os.environ["TEST_DATABASE_URI"]


class FlaskAppConfig:
    DEBUG = os.environ["FLASK_DEBUG"]
    SQLALCHEMY_ECHO = os.environ["FLASK_SQLALCHEMY_ECHO"]
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ["FLASK_SQLALCHEMY_TRACK_MODIFICATIONS"]

    SQLALCHEMY_DATABASE_URI = (
        DefaultConfig.TEST_DATABASE_URI
        if DefaultConfig.ENV == "test"
        else DefaultConfig.DATABASE_URI
    )

    SECRET_KEY = os.environ["SECRET_KEY"]
