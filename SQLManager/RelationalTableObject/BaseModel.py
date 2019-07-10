from flask_sqlalchemy import Model
import abc


class BaseModel(Model):

    id = None

    @classmethod
    @abc.abstractmethod
    def is_exist(cls, db_obj):
        ret = cls.query.filter(cls.id == db_obj.id).first()
        if ret is None:
            return False
        return True

    @classmethod
    @abc.abstractmethod
    def is_exist_id(cls, id):
        if id is not None:
            ret = cls.query.filter(cls.id == id).first()
            if ret is not None:
                return True
        return False
