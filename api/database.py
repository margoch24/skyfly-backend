from flask_sqlalchemy import SQLAlchemy
from singleton import SingletonMeta


class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.__db = None

    def initiate(self, app):
        self.__db = SQLAlchemy(app)

    def get_db(self):
        if not self.__db:
            raise Exception("Database not initialized. Call initiate() first.")
        return self.__db
