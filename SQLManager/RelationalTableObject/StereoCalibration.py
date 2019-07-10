# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.RelationalTableObject.Camera import Camera
from SQLManager.Exception.SqlException import ObjectNotExist


class StereoCalibration(sql_object.Model, BaseObject):

    __tablename__ = 'StereoCalibration'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    l_camera_id = sql_object.Column(sql_object.String(32), sql_object.ForeignKey('Camera.id'), nullable=True)

    r_camera_id = sql_object.Column(sql_object.String(32), sql_object.ForeignKey('Camera.id'), nullable=True)

    l_cam_matrix = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    r_cam_matrix = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    l_dist_coeffs = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    r_dist_coeffs = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    rt_cam_a2_cam_b = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    stereo_E = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    stereo_F = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    stereo_R = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    pixel_err = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    def __init__(self, l_camera_id, r_camera_id, l_cam_matrix=None, r_cam_matrix=None, l_dist_coeffs=None,
                 r_dist_coeffs=None, rt_cam_a2_cam_b=None, stereo_e=None, stereo_f=None, stereo_r=None, pixel_err=None):

        BaseObject.__init__(self)
        self._set_data(l_camera_id, r_camera_id, l_cam_matrix, r_cam_matrix, l_dist_coeffs, r_dist_coeffs,
                       rt_cam_a2_cam_b, stereo_e, stereo_f, stereo_r, pixel_err)

    def _set_data(self, l_camera_id, r_camera_id, l_cam_matrix=None, r_cam_matrix=None, l_dist_coeffs=None,
                  r_dist_coeffs=None, rt_cam_a2_cam_b=None, stereo_e=None, stereo_f=None, stereo_r=None,
                  pixel_err=None):

        if not Camera.is_exist_id(l_camera_id):
            raise ObjectNotExist("[Error]:camera is not exits which id is %s" % l_camera_id)
        if not Camera.is_exist_id(r_camera_id):
            raise ObjectNotExist("[Error]:camera is not exits which id is %s" % r_camera_id)
        self.l_camera_id = l_camera_id
        self.r_camera_id = r_camera_id
        self.l_cam_matrix = l_cam_matrix
        self.r_cam_matrix = r_cam_matrix
        self.l_dist_coeffs = l_dist_coeffs
        self.r_dist_coeffs = r_dist_coeffs
        self.rt_cam_a2_cam_b = rt_cam_a2_cam_b
        self.stereo_E = stereo_e
        self.stereo_F = stereo_f
        self.stereo_R = stereo_r
        self.pixel_err = pixel_err
