from marshmallow import Schema, fields, validate


class PostRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(8))
    name = fields.Str(required=True)
