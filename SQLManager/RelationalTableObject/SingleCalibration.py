# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class SingleCalibration(sql_object.Model, BaseObject):

    __tablename__ = 'SingleCalibration'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    camera_id = sql_object.relationship(
        "Camera",
        backref='SingleCalibration',
        lazy='dynamic',
        nullable=False
    )

    n_camera_args = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    p_camera_args = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    n_distortion_args = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    p_distortion_args = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    n_toc = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    p_toc = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    n_projection_err = sql_object.Column(sql_object.Double, nullable=True, unique=False)

    p_projection_err = sql_object.Column(sql_object.Double, nullable=True, unique=False)

    found_mask = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    img_pts = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    img_size = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    obj_pts = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    @classmethod
    def is_exist(cls, db_obj):
        ret = SingleCalibration.query.filter(SingleCalibration.id == db_obj.id).first()
        if ret is None:
            return False
        return True

    def __init__(self, id, camera_id, n_camera_args=None, p_camera_args=None, n_distortion_args=None,
                 p_distortion_args=None, n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None,
                 found_mask=None, img_pts=None, img_size=None, obj_pts=None):

        BaseObject.__init__(self)
        self._set_data(id, camera_id, n_camera_args, p_camera_args, n_distortion_args, p_distortion_args, n_toc,
                       p_toc, n_projection_err, p_projection_err, found_mask, img_pts, img_size, obj_pts)

    def _set_data(self, id, camera_id, n_camera_args=None, p_camera_args=None, n_distortion_args=None,
                  p_distortion_args=None, n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None,
                  found_mask=None, img_pts=None, img_size=None, obj_pts=None):

        self.id = id
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
