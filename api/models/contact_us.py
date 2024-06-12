from api.helpers.models import get_uuid
from api.models.base_model import BaseModel, db


class ContactUs(BaseModel):
    __tablename__ = "contact_us"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120))
    phone_number = db.Column(db.String(120))
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ContactUs {self.id}>"
