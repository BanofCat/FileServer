# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class InverseTest(sql_object.Model, BaseObject):

    __tablename__ = 'InverseTest'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    opt_all_ik = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    ik_err = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    l_cam_img_pts = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    r_cam_img_pts = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    pixel_err = sql_object.Column(sql_object.Double, nullable=True, unique=False)

    total_pixel_err = sql_object.Column(sql_object.Double, nullable=True, unique=False)

    @classmethod
    def is_exist(cls, db_obj):
        ret = InverseTest.query.filter(InverseTest.id == db_obj.id).first()
        if ret is None:
            return False
        return True

    def __init__(self, id, opt_all_ik=None, ik_err=None, l_cam_img_pts=None,
                 r_cam_img_pts=None, pixel_err=None, total_pixel_err=None):

        BaseObject.__init__(self)
        self._set_data(id, opt_all_ik, ik_err, l_cam_img_pts, r_cam_img_pts,
                       pixel_err, total_pixel_err)

    def _set_data(self, id, opt_all_ik=None, ik_err=None, l_cam_img_pts=None,
                  r_cam_img_pts=None, pixel_err=None, total_pixel_err=None):

        self.id = id
        self.opt_all_ik = opt_all_ik
        self.ik_err = ik_err
        self.l_cam_img_pts = l_cam_img_pts
        self.r_cam_img_pts = r_cam_img_pts
        self.pixel_err = pixel_err
        self.total_pixel_err = total_pixel_err
