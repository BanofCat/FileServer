# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.RelationalTableObject.Robot import Robot
from SQLManager.RelationalTableObject.User import User
from Exception.SqlException import ObjectNotExist


class GenerateData(sql_object.Model, BaseObject):

    __tablename__ = 'GenerateData'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    robot_id = sql_object.Column(sql_object.String(32), sql_object.ForeignKey('Robot.id'), nullable=False)

    user_id = sql_object.Column(sql_object.Integer, sql_object.ForeignKey('User.id'), nullable=False)

    pic_date = sql_object.Column(sql_object.DateTime, nullable=True, unique=False)

    dh_date = sql_object.Column(sql_object.DateTime, nullable=True, unique=False)

    fb_date = sql_object.Column(sql_object.DateTime, nullable=True, unique=False)

    def __init__(self, robot_id, user_id, pic_date=None, dh_date=None, fb_date=None):
        BaseObject.__init__(self)
        self.location_list = []
        self._set_data(robot_id, user_id, pic_date, dh_date, fb_date)

    def set_robot_id(self, robot_id):
        if not Robot.is_exist_id(robot_id):
            raise ObjectNotExist('%s is not exist which id is %s' % (Robot.__name__, robot_id))
        self.robot_id = robot_id

    def set_user_id(self, user_id):
        if not User.is_exist_id(user_id):
            raise ObjectNotExist('%s is not exist which id is %s' % (User.__name__, user_id))
        self.user_id = user_id

    def _set_data(self, robot_id, user_id, pic_date=None, dh_date=None, fb_date=None):
        self.set_robot_id(robot_id)
        self.set_user_id(user_id)
        self.pic_date = pic_date
        self.dh_date = dh_date
        self.fb_date = fb_date

    # def _init_location(self):
    #     SingleCalibration.query.filter(self.id == SingleCalibration.g_id)
    @classmethod
    def to_obj(cls, args_dict):
        for k in GenerateData.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_cam = GenerateData( args_dict[GenerateData.robot_id.name],
                                args_dict[GenerateData.user_id.name],
                                args_dict[GenerateData.pic_date.name],
                                args_dict[GenerateData.dh_date.name],
                                args_dict[GenerateData.fb_date.name]
                                )
        return new_cam

    @classmethod
    def update_obj(cls, args_dict):
        if GenerateData.id.name not in args_dict:
            raise ObjectNotExist('GenerateData id is wrong')
        gen = GenerateData.get_by_id(args_dict[GenerateData.id.name])
        if gen is None:
            raise ObjectNotExist('GenerateData id is wrong')

        # add origin data which are not in req data
        for k in GenerateData.__table__.columns:
            if k.name in args_dict:
                if k.name == GenerateData.robot_id.name:
                    gen.set_robot_id(args_dict[k.name])
                elif k.name == GenerateData.user_id.name:
                    gen.set_user_id(args_dict[k.name])
                else:
                    setattr(gen, k.name, args_dict[k.name])
        return gen


