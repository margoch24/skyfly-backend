from api.helpers.models import get_uuid
from api.models.base_model import BaseModel, db


class Review(BaseModel):
    __tablename__ = "reviews"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)

    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)

    user_id = db.Column(db.String(32), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.id}>"
