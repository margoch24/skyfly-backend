from database import Database
from flask_app import FlaskApp
from routes.auth_routes import auth_blueprint

from config import DefaultConfig, FlaskAppConfig

if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.set_config_object(FlaskAppConfig)

    db = Database()
    db.initiate(flask_app.app)

    flask_app.register_all_blueprints([auth_blueprint])

    flask_app.run(debug=FlaskAppConfig.DEBUG, port=DefaultConfig.PORT)
