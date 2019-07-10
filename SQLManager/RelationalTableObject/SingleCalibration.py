# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.RelationalTableObject.Camera import Camera
from SQLManager.Exception.SqlException import ObjectNotExist


class SingleCalibration(sql_object.Model, BaseObject):

    __tablename__ = 'SingleCalibration'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    camera_id = sql_object.Column(sql_object.String(32), sql_object.ForeignKey('Camera.id'), nullable=False)

    n_camera_args = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    p_camera_args = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    n_distortion_args = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    p_distortion_args = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    n_toc = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    p_toc = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    n_projection_err = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    p_projection_err = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    found_mask = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    img_pts = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    img_size = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    obj_pts = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    def __init__(self, camera_id, n_camera_args=None, p_camera_args=None, n_distortion_args=None,
                 p_distortion_args=None, n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None,
                 found_mask=None, img_pts=None, img_size=None, obj_pts=None):

        BaseObject.__init__(self)
        self._set_data(camera_id, n_camera_args, p_camera_args, n_distortion_args, p_distortion_args, n_toc,
                       p_toc, n_projection_err, p_projection_err, found_mask, img_pts, img_size, obj_pts)

    def _set_data(self, camera_id, n_camera_args=None, p_camera_args=None, n_distortion_args=None,
                  p_distortion_args=None, n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None,
                  found_mask=None, img_pts=None, img_size=None, obj_pts=None):

        if not Camera.is_exist_id(camera_id):
            raise ObjectNotExist("camera is not exits which id is %s" % camera_id)
        self.camera_id = camera_id
        self.n_camera_args = n_camera_args
        self.p_camera_args = p_camera_args
        self.n_distortion_args = n_distortion_args
        self.p_distortion_args = p_distortion_args
        self.n_toc = n_toc
        self.p_toc = p_toc
        self.n_projection_err = n_projection_err
        self.p_projection_err = p_projection_err
        self.found_mask = found_mask
        self.img_pts = img_pts
        self.img_size = img_size
        self.obj_pts = obj_pts
