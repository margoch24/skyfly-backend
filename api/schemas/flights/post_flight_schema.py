from marshmallow import Schema, fields, validate

from api.constants import CabinClass, Scheduled
from api.helpers.validation import class_props_to_arr


class PostFlightSchema(Schema):
    arrival = fields.Integer(required=True)
    photo = fields.Str()
    departure = fields.Integer(required=True)
    airline = fields.Str(required=True)
    cabin_class = fields.Str(
        required=True, validate=validate.OneOf(choices=class_props_to_arr(CabinClass))
    )
    scheduled = fields.Str(
        required=True, validate=validate.OneOf(choices=class_props_to_arr(Scheduled))
    )
    price = fields.Float(required=True)
    currency = fields.Str(required=True)
    from_longitude = fields.Float(required=True)
    from_latitude = fields.Float(required=True)

    to_longitude = fields.Float(required=True)
    to_latitude = fields.Float(required=True)
    score = fields.Float(required=True, validate=validate.Range(min=0, max=10))
