from flask import Blueprint, Flask, request
from flask_restful import Api, Resource

from config import DefaultConfig


class FlaskApp:

    @property
    def app(self) -> Flask:
        return self.__app

    @property
    def app_context(self):
        return self.__app_context

    @app.setter
    def app(self, app: Flask):
        self.__app = app

    def __init__(self) -> None:
        self.__app = Flask(__name__)
        self.__app_context = self.__app.app_context()
        self.cases_handling()

    def set_config(self, **configs):
        for config, value in configs:
            self.__app.config[config.upper()] = value

    def set_config_object(self, object):
        self.__app.config.from_object(object)

    def create_blueprint(self, name):
        return Blueprint(name, __name__)

    def create_api(self, bluprient):
        return Api(bluprient)

    def add_resource(self, api: Api, resource: Resource, endpoint=None):
        api.add_resource(resource, endpoint)

    def register_all_blueprints(self, blueprints=[]):
        for blueprint in blueprints:
            self.__app.register_blueprint(blueprint)

    def run(self, **kwargs):
        self.__app.run(**kwargs)

    def cases_handling(self):
        @self.__app.before_request
        def before_request():
            app_token = request.headers.get("app_token")
            if not app_token or app_token != DefaultConfig.APP_TOKEN:
                return {
                    "error": 1,
                    "data": {"message": "app_token is not specified in headers"},
                }, 400
