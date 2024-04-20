from responses.services import ServiceResponse


class AuthService:
    def post_login(email: str, password: str):
        print("aaaa")

        response = {"error": 0, "data": {"email": email, "password": password}}
        return ServiceResponse(status=200, response=response)
