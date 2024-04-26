from api.constants import Scheduled
from api.helpers.models import get_uuid
from api.models.base_model import BaseModel, db


class Flight(BaseModel):
    __tablename__ = "flights"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    departure = db.Column(db.BigInteger, nullable=False)
    arrival = db.Column(db.BigInteger, nullable=False)
    photo = db.Column(db.String(225))
    airline = db.Column(db.String(120))
    cabin_class = db.Column(db.String(120))
    scheduled = db.Column(db.String(120), default=Scheduled.ONCE)

    price = db.Column(db.Float(precision=32, decimal_return_scale=None))
    currency = db.Column(db.String(4))

    longitude = db.Column(db.Float(precision=32, decimal_return_scale=None))
    latitude = db.Column(db.Float(precision=32, decimal_return_scale=None))

    score = db.Column(db.Float)

    is_deleted = db.Column(db.Boolean, default=False)

    tickets = db.relationship("Ticket", back_populates="flight")

    def __repr__(self):
        return f"<Flight {self.id}>"
