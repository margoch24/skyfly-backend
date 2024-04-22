from api.bcrypt_flask import FlaskBcrypt
from api.database import Database
from api.flask_app import FlaskApp
from api.jwt_flask import FlaskJWT
from config import DefaultConfig, FlaskAppConfig

flask_app = FlaskApp()
flask_app.set_config_object(FlaskAppConfig)

db = Database()
db.initiate(flask_app.app)

bcrypt = FlaskBcrypt()
bcrypt.initiate(flask_app.app)

jwt = FlaskJWT()
jwt.initiate(flask_app.app)

from api.routes.auth_routes import auth_blueprint
from api.routes.contact_us_routes import contact_us_blueprint
from api.routes.reviews_routes import reviews_blueprint
from api.routes.user_routes import user_blueprint

flask_app.register_all_blueprints(
    [auth_blueprint, user_blueprint, reviews_blueprint, contact_us_blueprint]
)

with flask_app.app_context:
    db.create_all()


if __name__ == "__main__":
    flask_app.run(debug=FlaskAppConfig.DEBUG, port=DefaultConfig.PORT)
