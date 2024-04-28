from api.constants import DEFAULT_LIMIT
from api.database import Database
from api.helpers import current_milli_time

db = Database().get_db()


class BaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.BigInteger, default=current_milli_time)
    updated_at = db.Column(
        db.BigInteger, default=current_milli_time, onupdate=current_milli_time
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
    def find(
        cls,
        condition=None,
        limit=None,
        order_by: list = None,
        join: list[dict] = None,
        comparative_condition: list = None,
        page: int = None,
    ):
        query = db.session.query(cls)

        if join:
            for join_table in join:
                query = query.join(join_table["table"], join_table["condition"])

        if condition:
            query = query.filter_by(**condition)

        if comparative_condition:
            query = query.filter(*comparative_condition)

        if order_by:
            query = query.order_by(*order_by)

        if page:
            query = query.offset(page * (limit or DEFAULT_LIMIT))

        if limit:
            query = query.limit(limit)

        return query.all()

    @classmethod
    def find_one(
        cls,
        condition=None,
        comparative_condition=None,
        join: list[dict] = None,
    ):
        query = db.session.query(cls)

        if join:
            for join_table in join:
                query = query.join(join_table["table"], join_table["condition"])

        if condition:
            query = query.filter_by(**condition)

        if comparative_condition:
            query = query.filter(*comparative_condition)

        return query.first()

    def serialize(self, exclude_fields=[]):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in exclude_fields
        }
