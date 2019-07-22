# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist
from SQLManager.RelationalTableObject.LocationList import LocationList


class InverseTest(sql_object.Model, BaseObject):

    __tablename__ = 'InverseTest'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    opt_all_ik = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    ik_err = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    l_cam_img_pts = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    r_cam_img_pts = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    pixel_err = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    total_pixel_err = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    def __init__(self, opt_all_ik=None, ik_err=None, l_cam_img_pts=None,
                 r_cam_img_pts=None, pixel_err=None, total_pixel_err=None, loc_obj=None):

        BaseObject.__init__(self)
        self._set_data(opt_all_ik, ik_err, l_cam_img_pts, r_cam_img_pts,
                       pixel_err, total_pixel_err, loc_obj)

    def _set_data(self, opt_all_ik=None, ik_err=None, l_cam_img_pts=None,
                  r_cam_img_pts=None, pixel_err=None, total_pixel_err=None, loc_obj=None):

        self.opt_all_ik = opt_all_ik
        self.ik_err = ik_err
        self.l_cam_img_pts = l_cam_img_pts
        self.r_cam_img_pts = r_cam_img_pts
        self.pixel_err = pixel_err
        self.total_pixel_err = total_pixel_err

    @classmethod
    def to_obj(cls, args_dict):
        if LOCATION_ID_N not in args_dict:
            raise ObjectNotExist('Location id is wrong')
        location_obj = LocationList.get_by_id(args_dict[LOCATION_ID_N])
        if location_obj is None:
            raise ObjectNotExist('Location id is wrong')

        for k in InverseTest.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_dh = InverseTest(  args_dict[InverseTest.opt_all_ik.name],
                               args_dict[InverseTest.ik_err.name],
                               args_dict[InverseTest.l_cam_img_pts.name],
                               args_dict[InverseTest.r_cam_img_pts.name],
                               args_dict[InverseTest.pixel_err.name],
                               args_dict[InverseTest.total_pixel_err.name],
                               location_obj
                               )
        return new_dh

    @classmethod
    def update_obj(cls, args_dict, location_obj):
        if location_obj is None:
            raise ObjectNotExist('Location id is wrong')
        if InverseTest.id.name not in args_dict:
            raise ObjectNotExist('InverseTest id is wrong')
        dh_obj = InverseTest.get_by_id(args_dict[InverseTest.id.name])
        if dh_obj is None:
            raise ObjectNotExist('InverseTest id is wrong')

        # add origin data which are not in req data
        for k in InverseTest.__table__.columns:
            if k.name in args_dict:
                setattr(dh_obj, k.name, args_dict[k.name])
        return dh_obj

