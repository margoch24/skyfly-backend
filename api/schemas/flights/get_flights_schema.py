from marshmallow import Schema, fields, validate

from api.constants import CabinClass
from api.helpers.validation import (
    cabin_class_validation,
    class_props_to_arr,
    price_range_validation,
)


class GetFlightsSchema(Schema):
    longitude = fields.Float()
    latitude = fields.Float()
    departure = fields.Integer()
    arrival = fields.Integer()
    cabin_class = fields.String(validate=cabin_class_validation)
    price = fields.String(validate=price_range_validation)
    page = fields.Integer()
    limit = fields.Integer()
