from api.helpers.models import get_uuid
from api.models.base_model import BaseModel, db


class Ticket(BaseModel):
    __tablename__ = "tickets"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    date_of_birth = db.Column(db.DateTime)

    price = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(4), nullable=False)

    is_deleted = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="tickets")

    seat_id = db.Column(db.String(32), db.ForeignKey("seats.id"), nullable=False)
    seat = db.relationship("Seat", back_populates="tickets")

    flight_id = db.Column(db.String(32), db.ForeignKey("flights.id"), nullable=False)
    flight = db.relationship("Flight", back_populates="tickets")

    def __repr__(self):
        return f"<Ticket {self.id}>"
