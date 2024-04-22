from api.helpers import get_uuid
from api.models.base_model import BaseModel, db


class User(BaseModel):
    __exclude_fields = ["password", "refresh_token"]
    __tablename__ = "users"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    photo = db.Column(db.String(225))
    refresh_token = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.id}>"

    def serialize(self, exclude_fields: list[str] = []):
        return super().serialize([*exclude_fields, *self.__exclude_fields])
