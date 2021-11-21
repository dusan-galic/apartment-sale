from core import db

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import func

from datetime import datetime, date
from dateutil import parser


class BaseModel(object):

    @declared_attr
    def id(self):
        return db.Column(db.Integer, primary_key=True, autoincrement=True)

    @declared_attr
    def date_of_creation(self):
        return db.deferred(db.Column(db.DateTime, nullable=False, server_default=func.now()))

    @declared_attr
    def date_of_update(self):
        return db.deferred(
            db.Column(db.DateTime, nullable=False, onupdate=func.now(), server_default=func.now()))

    @declared_attr
    def deleted(self):
        return db.deferred(db.Column(db.Boolean, server_default=db.false(), default=False))

    @classmethod
    def get_by_id(cls, _id):
        if hasattr(cls, "query"):
            return cls.query.get(_id)

    def edit(self, set_nulls=False, **kwargs):
        if isinstance(self, db.Model):
            edit_sqlalchemy_object(self, set_nulls, **kwargs)

    @classmethod
    def create(cls, **kwargs):
        create_obj = cls()
        edit_sqlalchemy_object(create_obj, **kwargs)
        create_obj.date_of_creation = datetime.utcnow()
        return create_obj


class NotSQLAlchemyObjectError(Exception):
    pass


def edit_sqlalchemy_object(obj, set_nulls=False, **kwargs):
    if not hasattr(obj, '__table__'):
        raise NotSQLAlchemyObjectError('object myst have __table__ property')
    for arg in kwargs:
        if hasattr(obj, arg) and (set_nulls or kwargs.get(arg) is not None) and arg in obj.__table__.c:
            # need to think of better way to check for boolean values
            if kwargs.get(arg) in ['true', 'false', 'True', 'False']:
                setattr(obj, arg, kwargs.get(arg) in ['true', 'True'])
            elif obj.__table__.c[arg].type.python_type in [datetime, date]:
                if type(kwargs.get(arg)) == str:
                    setattr(obj, arg, parser.parse(kwargs.get(arg)))
                elif type(kwargs.get(arg)) in [date, datetime]:
                    setattr(obj, arg, kwargs.get(arg))
                elif set_nulls and kwargs.get(arg) is None:
                    setattr(obj, arg, kwargs.get(arg))
                else:
                    # TODO raise error
                    pass
            elif type(kwargs.get(arg)) == list and type(obj.__table__.c[arg].type) == db.JSON:
                setattr(obj, arg, kwargs.get(arg))
            else:
                if kwargs.get(arg) is None:
                    if set_nulls:
                        setattr(obj, arg, None)
                else:
                    setattr(obj, arg, obj.__table__.c[arg].type.python_type(kwargs.get(arg)))
    if hasattr(obj, 'date_of_update'):
        setattr(obj, 'date_of_update', datetime.utcnow())