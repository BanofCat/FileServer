# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class Robot(sql_object.Model, BaseObject):

    __tablename__ = 'Robot'

    id = sql_object.Column(sql_object.String(32), primary_key=True)

    joints = sql_object.Column(sql_object.Integer, unique=False, nullable=False)

    type = sql_object.Column(sql_object.Enum("RR", "KENT", "DDR"), nullable=False, unique=False)

    def __init__(self, id, joints, type):
        BaseObject.__init__(self)
        self._set_data(id, joints, type)

    def _set_data(self, id, joints, type):
        self.id = id
        self.joints = joints
        self.type = type

    @classmethod
    def to_obj(cls, args_dict):
        for k in Robot.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_rob = Robot(args_dict[Robot.id.name],
                        args_dict[Robot.joints.name],
                        args_dict[Robot.type.name]
                        )
        return new_rob
