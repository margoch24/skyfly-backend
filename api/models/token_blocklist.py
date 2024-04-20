from api.helpers.get_uuid import get_uuid
from api.models.base_model import BaseModel, db


class TokenBlocklist(BaseModel):
    __tablename__ = "tokens_blocklist"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    jti = db.Column(db.String(36), nullable=False)
    type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Token {self.id}>"
