from marshmallow import Schema, fields, validate


class PostLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(8))
