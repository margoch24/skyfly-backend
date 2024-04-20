from helpers.request_validator import (
    BodyRequestValidator,
    QueryRequestValidator,
    RequestValidatorTypes,
)

REQUEST_VALIDATOR_CLASSES = {
    RequestValidatorTypes.Body: BodyRequestValidator,
    RequestValidatorTypes.Query: QueryRequestValidator,
}
