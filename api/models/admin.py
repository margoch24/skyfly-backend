from api.helpers.get_uuid import get_uuid
from api.models.base_model import BaseModel, db


class Admin(BaseModel):
    __tablename__ = "admins"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Admin {self.id}>"
