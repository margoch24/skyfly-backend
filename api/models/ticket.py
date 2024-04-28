from api.constants import TicketType
from api.helpers.models import get_uuid
from api.models.base_model import BaseModel, db


class Ticket(BaseModel):
    __tablename__ = "tickets"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    date_of_birth = db.Column(db.BigInteger)
    type = db.Column(db.String(120), default=TicketType.ADULT)
    qrcode = db.Column(db.String(225))

    price = db.Column(db.Float(precision=32, decimal_return_scale=None), nullable=False)
    currency = db.Column(db.String(4), nullable=False)

    is_deleted = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="ticket")

    seat_id = db.Column(db.String(32), db.ForeignKey("seats.id"), nullable=False)
    seat = db.relationship("Seat", back_populates="ticket")

    flight_id = db.Column(db.String(32), db.ForeignKey("flights.id"), nullable=False)
    flight = db.relationship("Flight", back_populates="ticket")

    def __repr__(self):
        return f"<Ticket {self.id}>"
