# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class DH_Optimised(sql_object.Model, BaseObject):

    __tablename__ = 'DH_Optimised'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    model = sql_object.Column(sql_object.Enum("SM", "Faset"), nullable=False, unique=False)

    angle_offset_full = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    joint_scale_factor = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    refine_pixel_err = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    robot_param = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    tot = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    trc = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    a_offset_six_param = sql_object.Column(sql_object.Double, nullable=True, unique=False)

    c_offset_six_param = sql_object.Column(sql_object.Double, nullable=True, unique=False)

    @classmethod
    def is_exist(cls, db_obj):
        ret = DH_Optimised.query.filter(DH_Optimised.id == db_obj.id).first()
        if ret is None:
            return False
        return True

    def __init__(self, id, model, angle_offset_full=None, joint_scale_factor=None, refine_pixel_err=None,
                 robot_param=None, tot=None, trc=None, a_offset_six_param=None, c_offset_six_param=None):

        BaseObject.__init__(self)
        self._set_data(id, model, angle_offset_full, joint_scale_factor, refine_pixel_err, robot_param,
                       tot, trc, a_offset_six_param, c_offset_six_param)

    def _set_data(self, id, model, angle_offset_full=None, joint_scale_factor=None, refine_pixel_err=None,
                  robot_param=None, tot=None, trc=None, a_offset_six_param=None, c_offset_six_param=None):

        self.id = id
        self.model = model
        self.angle_offset_full = angle_offset_full
        self.joint_scale_factor = joint_scale_factor
        self.refine_pixel_err = refine_pixel_err
        self.robot_param = robot_param
        self.tot = tot
        self.trc = trc
        self.a_offset_six_param = a_offset_six_param
        self.c_offset_six_param = c_offset_six_param
