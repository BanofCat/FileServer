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
                 robot_param=None, tot=None, trc=None, a_offset_six_param=None, c_offset_six_param=None, loc_obj=None):

        BaseObject.__init__(self)
        self.set_location(loc_obj)
        self._set_data(model, angle_offset_full, joint_scale_factor, refine_pixel_err, robot_param,
                       tot, trc, a_offset_six_param, c_offset_six_param)

    def _set_data(self, model, angle_offset_full=None, joint_scale_factor=None, refine_pixel_err=None,
                  robot_param=None, tot=None, trc=None, a_offset_six_param=None, c_offset_six_param=None):

        self.set_model(model)
        self.angle_offset_full = self.to_uri(angle_offset_full)
        self.joint_scale_factor = self.to_uri(joint_scale_factor)
        self.refine_pixel_err = self.to_uri(refine_pixel_err)
        self.robot_param = self.to_uri(robot_param)
        self.tot = self.to_uri(tot)
        self.trc = self.to_uri(trc)
        self.a_offset_six_param = self.to_uri(a_offset_six_param)
        self.c_offset_six_param = self.to_uri(c_offset_six_param)

    def to_uri(self, filename):
        if filename is None:
            return None
        abs_path = self.location_obj.get_upload_path() + self.__class__.__name__ + '/' + filename
        if not os.path.exists(abs_path):
            print('set uri failed: ', abs_path)
            raise ObjectNotExist("%s file is not exist, please upload first" % filename)
        return DOWNLOAD_ROOT_URI + str(self.location_obj.id) + '/' + self.__class__.__name__ + '/' + filename

    def set_location(self, loc_obj):
        self.location_obj = loc_obj

    def set_model(self, model):
        if model not in DH_Model.__dict__.keys():
            raise ObjectNotExist("mode should be one of %s" % list(DH_Model))
        self.model = model


    @classmethod
    def to_obj(cls, args_dict, location_obj):
        for k in DH_Optimised.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_dh = DH_Optimised( args_dict[DH_Optimised.model.name],
                               args_dict[DH_Optimised.angle_offset_full.name],
                               args_dict[DH_Optimised.joint_scale_factor.name],
                               args_dict[DH_Optimised.refine_pixel_err.name],
                               args_dict[DH_Optimised.robot_param.name],
                               args_dict[DH_Optimised.tot.name],
                               args_dict[DH_Optimised.trc.name],
                               args_dict[DH_Optimised.a_offset_six_param.name],
                               args_dict[DH_Optimised.c_offset_six_param.name],
                               location_obj
                               )
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
        dh_obj.set_location(location_obj)
        # add origin data which are not in req data
        for k in DH_Optimised.__table__.columns:
            if k.name in args_dict and args_dict[k.name] is not None:
                if k.name == cls.model.name:
                    dh_obj.set_model(args_dict[k.name])
                elif k.name == cls.angle_offset_full.name or    \
                     k.name == cls.joint_scale_factor.name or   \
                     k.name == cls.refine_pixel_err.name or     \
                     k.name == cls.robot_param.name or          \
                     k.name == cls.tot.name or                  \
                     k.name == cls.trc.name:
                    setattr(dh_obj, k.name, dh_obj.to_uri(args_dict[k.name]))
                else:
                    setattr(dh_obj, k.name, args_dict[k.name])
        return dh_obj
