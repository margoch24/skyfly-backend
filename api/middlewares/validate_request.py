from api.constants import REQUEST_VALIDATOR_CLASSES
from api.helpers.request_validator import QueryRequestValidator, RequestValidator


def validate_request(Schema, validator_type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            validator: RequestValidator = REQUEST_VALIDATOR_CLASSES.get(
                validator_type, QueryRequestValidator
            )(Schema())

            errors = validator.validate()
            if errors:
                return {"error": 1, "data": errors}, 400

            return func(*args, **kwargs)

        return wrapper

    return decorator
