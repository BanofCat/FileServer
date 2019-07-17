# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.RelationalTableObject.Robot import Robot
from SQLManager.RelationalTableObject.User import User
from Exception import ObjectNotExist


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

    def _set_data(self, robot_id, user_id, pic_date=None, dh_date=None, fb_date=None):
        if not Robot.is_exist_id(robot_id):
            raise ObjectNotExist("[Error]:robot is not exits which id is %s" % robot_id)
        if not User.is_exist_id(user_id):
            raise ObjectNotExist("[Error]:user is not exits which id is %s" % user_id)
        self.robot_id = robot_id
        self.user_id = user_id
        self.pic_date = pic_date
        self.dh_date = dh_date
        self.fb_date = fb_date

    # def _init_location(self):
    #     SingleCalibration.query.filter(self.id == SingleCalibration.g_id)






