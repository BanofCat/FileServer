# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.RelationalTableObject.SingleCalibration import SingleCalibration


class GenerateData(sql_object.Model, BaseObject):

    __tablename__ = 'GenerateData'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    robot_id = sql_object.relationship(
        'Robot',
        backref='GenerateData',
        lazy='dynamic'
    )

    user_id = sql_object.relationship(
        'User',
        backref='GenerateData',
        lazy='dynamic'
    )

    pic_date = sql_object.Column(sql_object.DateTime, nullable=True, unique=False)

    dh_date = sql_object.Column(sql_object.DateTime, nullable=True, unique=False)

    fb_date = sql_object.Column(sql_object.DateTime, nullable=True, unique=False)

    @classmethod
    def is_exist(cls, db_obj):
        ret = GenerateData.query.filter(GenerateData.id == db_obj.id).first()
        if ret is None:
            return False
        return True

    def __init__(self, id, robot_id, user_id, pic_date=None, dh_date=None, fb_date=None):
        BaseObject.__init__(self)
        self.location_list = []
        self._set_data(id, robot_id, user_id, pic_date, dh_date, fb_date)

    def _set_data(self, id, robot_id, user_id, pic_date=None, dh_date=None, fb_date=None):
        self.id = id
        self.robot_id = robot_id
        self.user_id = user_id
        self.pic_date = pic_date
        self.dh_date = dh_date
        self.fb_date = fb_date

    def _init_location(self):
        SingleCalibration.query.filter(self.id == SingleCalibration.g_id)






