from flask_sqlalchemy import SQLAlchemy

from api.singleton_meta import SingletonMeta


class Database(metaclass=SingletonMeta):

    def __init__(self):
        self.__db = None

    def initiate(self, app):
        self.__db = SQLAlchemy(app)

    def create_all(self):
        self.__db.create_all()

    def drop_all(self):
        self.__db.session.remove()
        self.__db.drop_all()

    def get_db(self):
        if not self.__db:
            raise Exception("Database not initialized. Call initiate() first.")
        return self.__db
