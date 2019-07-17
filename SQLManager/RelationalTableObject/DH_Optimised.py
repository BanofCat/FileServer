# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from Exception import ObjectNotExist
import enum


class DH_Model(enum.Enum):

    SM = 'SM'
    Faset = 'Faset'


class DH_Optimised(sql_object.Model, BaseObject):

    __tablename__ = 'DH_Optimised'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    model = sql_object.Column(sql_object.Enum(DH_Model), nullable=False, unique=False)

    angle_offset_full = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    joint_scale_factor = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    refine_pixel_err = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    robot_param = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    tot = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    trc = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    a_offset_six_param = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    c_offset_six_param = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    def __init__(self, model, angle_offset_full=None, joint_scale_factor=None, refine_pixel_err=None,
                 robot_param=None, tot=None, trc=None, a_offset_six_param=None, c_offset_six_param=None):

        BaseObject.__init__(self)
        self._set_data(model, angle_offset_full, joint_scale_factor, refine_pixel_err, robot_param,
                       tot, trc, a_offset_six_param, c_offset_six_param)

    def _set_data(self, model, angle_offset_full=None, joint_scale_factor=None, refine_pixel_err=None,
                  robot_param=None, tot=None, trc=None, a_offset_six_param=None, c_offset_six_param=None):

        if not isinstance(model, DH_Model):
            raise ObjectNotExist("%s is not a recognized model" % model)
        self.model = model
        self.angle_offset_full = angle_offset_full
        self.joint_scale_factor = joint_scale_factor
        self.refine_pixel_err = refine_pixel_err
        self.robot_param = robot_param
        self.tot = tot
        self.trc = trc
        self.a_offset_six_param = a_offset_six_param
        self.c_offset_six_param = c_offset_six_param
