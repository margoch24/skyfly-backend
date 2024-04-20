from flask_bcrypt import Bcrypt


class FlaskBcrypt:

    def __init__(self):
        self.__bcrypt = Bcrypt()

    def initiate(self, app):
        self.__bcrypt = Bcrypt(app)

    def hash_password(self, password):
        try:
            hashed_password = self.__bcrypt.generate_password_hash(password).decode(
                "utf-8"
            )
            return hashed_password
        except Exception as e:
            print(f"ERROR (bcrypt hash_password): {e}")
            return None

    def check_password(self, password, input_password):
        try:
            isValid = self.__bcrypt.check_password_hash(password, input_password)
            return isValid
        except Exception as e:
            print(f"ERROR (bcrypt check_password): {e}")
            return False
