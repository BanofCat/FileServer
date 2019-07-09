# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class Robot(sql_object.Model, BaseObject):

    __tablename__ = 'Robot'

    id = sql_object.Column(sql_object.String(32), primary_key=True)

    joints = sql_object.Column(sql_object.Tinyint, unique=False, nullable=False)

    type = sql_object.Column(sql_object.Enum("RR", "KENT", "DDR"), nullable=False, unique=False)

    @classmethod
    def is_exist(cls, db_obj):
        ret = Robot.query.filter(Robot.id == db_obj.id).first()
        if ret is None:
            return False
        return True

    def __init__(self, id, joints, type):
        BaseObject.__init__(self)
        self._set_data(id, joints, type)

    def _set_data(self, id, joints, type):
        self.id = id
        self.joints = joints
        self.type = type
