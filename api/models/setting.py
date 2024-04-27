from api.helpers.models import get_uuid
from api.models.base_model import BaseModel, db


class Setting(BaseModel):
    __tablename__ = "settings"

    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)

    key = db.Column(db.String(64))
    value = db.Column(db.String(120))
    description = db.Column(db.Text)

    is_deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Setting {self.id}>"
