from api.helpers.models import get_uuid
from api.models.base_model import BaseModel, db


class Seat(BaseModel):
    __tablename__ = "seats"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.String(4), nullable=False)
    type = db.Column(db.String(120), nullable=False)
    cabin_class = db.Column(db.String(120))

    is_deleted = db.Column(db.Boolean, default=False)

    tickets = db.relationship("Ticket", back_populates="seat")

    def __repr__(self):
        return f"<Seat {self.id}>"
