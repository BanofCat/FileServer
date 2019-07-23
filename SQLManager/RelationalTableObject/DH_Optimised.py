# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from Exception.SqlException import ObjectNotExist
import enum
from Configure.HttpSetting import *


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

    @classmethod
    def to_obj(cls, args_dict):
        # if LOCATION_ID_N not in args_dict:
        #     raise ObjectNotExist('Location id is wrong')
        # dh_obj = DH_Optimised.get_by_id(args_dict[LOCATION_ID_N])
        # if dh_obj is None:
        #     raise ObjectNotExist('Location id is wrong')
        #
        # for k in DH_Optimised.__table__.columns:
        #     if k.name not in args_dict:
        #         args_dict[k.name] = None
        #
        # new_dh = DH_Optimised( args_dict[DH_Optimised.model.name],
        #                            args_dict[DH_Optimised.angle_offset_full.name],
        #                            args_dict[DH_Optimised.joint_scale_factor.name],
        #                            args_dict[DH_Optimised.refine_pixel_err.name],
        #                            args_dict[DH_Optimised.tot.name],
        #                            args_dict[DH_Optimised.trc.name],
        #                            args_dict[DH_Optimised.a_offset_six_param.name],
        #                            args_dict[DH_Optimised.c_offset_six_param.name],
        #                            location_obj
        #                            )
        return new_dh

    @classmethod
    def update_obj(cls, args_dict, location_obj):
        if location_obj is None:
            raise ObjectNotExist('Location id is wrong')
        if DH_Optimised.id.name not in args_dict:
            raise ObjectNotExist('DH_Optimised id is wrong')
        dh_obj = DH_Optimised.get_by_id(args_dict[DH_Optimised.id.name])
        if dh_obj is None:
            raise ObjectNotExist('DH_Optimised id is wrong')

        # add origin data which are not in req data
        for k in DH_Optimised.__table__.columns:
            if k.name in args_dict:
                setattr(dh_obj, k.name, args_dict[k.name])
        return dh_obj
