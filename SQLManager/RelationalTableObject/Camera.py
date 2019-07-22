# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class Camera(sql_object.Model, BaseObject):

    __tablename__ = 'Camera'

    id = sql_object.Column(sql_object.String(32), primary_key=True)

    use_type = sql_object.Column(sql_object.String(32), unique=False, nullable=False)

    producer = sql_object.Column(sql_object.String(32), nullable=True, unique=False)

    def __init__(self, id, use_type, producer):
        BaseObject.__init__(self)
        self._set_data(id, use_type, producer)

    def _set_data(self, id, use_type, producer):
        self.id = id
        self.use_type = use_type
        self.producer = producer

    @classmethod
    def to_obj(cls, args_dict):
        for k in Camera.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_cam = Camera(args_dict[Camera.id.name],
                         args_dict[Camera.use_type.name],
                         args_dict[Camera.producer.name]
                         )
        return new_cam



