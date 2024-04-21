from marshmallow import Schema, fields, validate


class PostReviewSchema(Schema):
    rating = fields.Integer(required=True, validate=validate.Range(min=0, max=5))
    message = fields.Str(required=True)
