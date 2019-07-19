# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.RelationalTableObject.Camera import Camera
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist


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
                 found_mask=None, img_pts=None, img_size=None, obj_pts=None, req_user=None):

        BaseObject.__init__(self)
        self._set_data(camera_id, n_camera_args, p_camera_args, n_distortion_args, p_distortion_args, n_toc,
                       p_toc, n_projection_err, p_projection_err, found_mask, img_pts, img_size, obj_pts, req_user)

    def _set_data(self, camera_id, n_camera_args=None, p_camera_args=None, n_distortion_args=None,
                  p_distortion_args=None, n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None,
                  found_mask=None, img_pts=None, img_size=None, obj_pts=None, req_user=None):

        self.camera_id = self._set_cam(camera_id)
        self.n_camera_args = self._set_uri(req_user, n_camera_args)
        self.p_camera_args = self._set_uri(req_user, p_camera_args)
        self.n_distortion_args = self._set_uri(req_user, n_distortion_args)
        self.p_distortion_args = self._set_uri(req_user, p_distortion_args)
        self.n_toc = self._set_uri(req_user, n_toc)
        self.p_toc = self._set_uri(req_user, p_toc)
        self.n_projection_err = n_projection_err
        self.p_projection_err = p_projection_err
        self.found_mask = self._set_uri(req_user, found_mask)
        self.img_pts = self._set_uri(req_user, img_pts)
        self.img_size = self.set_size(img_size)
        self.obj_pts = self._set_uri(req_user, obj_pts)

    def _set_uri(self, req_user, filename):
        if filename is None:
            return None
        abs_path = req_user.get_upload_path() + filename
        if not os.path.exists(abs_path):
            print('set uri failed: ', abs_path)
            raise ObjectNotExist("%s file is not exist, please upload first" % filename)
        return DOWNLOAD_ROOT_URI + filename

    def _set_cam(self, cam_id):
        if not Camera.is_exist_id(cam_id):
            raise ObjectNotExist("camera is not exits which id is %s" % cam_id)
        return cam_id

    def set_size(self, size_arr):
        return str(size_arr)

    @classmethod
    def to_obj(cls, args_dict, req_user=None):
        for k in SingleCalibration.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_stereo = SingleCalibration(args_dict[SingleCalibration.l_camera_id.name],
                                       args_dict[SingleCalibration.r_camera_id.name],
                                       args_dict[SingleCalibration.l_cam_matrix.name],
                                       args_dict[SingleCalibration.r_cam_matrix.name],
                                       args_dict[SingleCalibration.l_dist_coeffs.name],
                                       args_dict[SingleCalibration.r_dist_coeffs.name],
                                       args_dict[SingleCalibration.rt_cam_a2_cam_b.name],
                                       args_dict[SingleCalibration.stereo_E.name],
                                       args_dict[SingleCalibration.stereo_F.name],
                                       args_dict[SingleCalibration.stereo_R.name],
                                       args_dict[SingleCalibration.pixel_err.name],
                                       req_user
                                       )
        return new_stereo
