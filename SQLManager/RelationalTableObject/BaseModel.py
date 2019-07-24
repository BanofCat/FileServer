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

    @classmethod
    @abc.abstractmethod
    def get_by_id(cls, id=-1):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    @abc.abstractmethod
    def get_all_gen_list(cls):
        return cls.query.all()

    @classmethod
    @abc.abstractmethod
    def update_obj(cls, args_dict):
        if cls.id.name not in args_dict:
            print('id is none')
            return None
        obj = cls.get_by_id(args_dict[cls.id.name])
        if obj is not None:
            for k in cls.__table__.columns:
                if k.name in args_dict and args_dict[k.name] is not None:
                    setattr(obj, k.name, args_dict[k.name])

        print(cls.to_dict(obj))
        return obj
