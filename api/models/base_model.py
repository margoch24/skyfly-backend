from datetime import datetime, timezone

from api.database import Database

db = Database().get_db()


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.String(120), default=str(datetime.now()))
    updated_at = db.Column(
        db.String(120),
        default=str(datetime.now()),
        onupdate=str(datetime.now()),
    )

    @classmethod
    def create(cls, **kwargs):
        record = cls(**kwargs)
        db.session.add(record)
        db.session.commit()
        return record

    @classmethod
    def update_one(cls, record_id, **kwargs):
        record = db.session.get(cls, record_id)

        if record is None:
            return record

        for key, value in kwargs.items():
            setattr(record, key, value)

        db.session.commit()
        return record

    @classmethod
    def update(cls, condition=None, **kwargs):
        query = db.session.query(cls)

        if condition:
            query = query.filter_by(**condition)

        records = query.all()
        if len(records) <= 0:
            return None

        for record in records:
            for key, value in kwargs.items():
                setattr(record, key, value)

        db.session.commit()
        return records

    @classmethod
    def delete(cls, condition=None):
        query = db.session.query(cls)
        if condition:
            query = query.filter_by(**condition)

        records = query.all()
        if len(records) <= 0:
            return False

        for record in records:
            db.session.delete(record)

        db.session.commit()
        return True

    @classmethod
    def delete_one(cls, record_id):
        record = db.session.get(cls, record_id)
        if record is None:
            return False

        db.session.delete(record)
        db.session.commit()
        return True

    @classmethod
    def find(cls, condition=None, limit=None):
        query = db.session.query(cls)
        if condition:
            query = query.filter_by(**condition)

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    @classmethod
    def find_one(cls, condition=None):
        query = db.session.query(cls)
        if condition:
            return query.filter_by(**condition).first()

        return query.first()

    def serialize(self, exclude_fields=[]):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in exclude_fields
        }
