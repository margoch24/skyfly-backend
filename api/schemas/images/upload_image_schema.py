from marshmallow import Schema, fields


class UploadImageSchema(Schema):
    file = fields.Field(required=True)
