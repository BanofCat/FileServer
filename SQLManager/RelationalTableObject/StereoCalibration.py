# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.RelationalTableObject.Camera import Camera
from Exception.SqlException import ObjectNotExist
from SQLManager.RelationalTableObject.User import User
from Configure.HttpSetting import *


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

    stereo_F = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    stereo_R = sql_object.Column(sql_object.String(256), nullable=True, unique=False)

    pixel_err = sql_object.Column(sql_object.Float(20, 10), nullable=True, unique=False)

    def __init__(self, l_camera_id, r_camera_id, l_cam_matrix=None, r_cam_matrix=None, l_dist_coeffs=None,
                 r_dist_coeffs=None, rt_cam_a2_cam_b=None, stereo_e=None, stereo_f=None, stereo_r=None, pixel_err=None,
                 req_user=None):

        BaseObject.__init__(self)
        self._set_data(l_camera_id, r_camera_id, l_cam_matrix, r_cam_matrix, l_dist_coeffs, r_dist_coeffs,
                       rt_cam_a2_cam_b, stereo_e, stereo_f, stereo_r, pixel_err, req_user)

    def _set_data(self, l_camera_id, r_camera_id, l_cam_matrix=None, r_cam_matrix=None, l_dist_coeffs=None,
                  r_dist_coeffs=None, rt_cam_a2_cam_b=None, stereo_e=None, stereo_f=None, stereo_r=None,
                  pixel_err=None, req_user=None):

        self.l_camera_id = self._set_cam(l_camera_id)
        self.r_camera_id = self._set_cam(r_camera_id)
        if req_user is not None:
            self.l_cam_matrix = self._set_uri(req_user, l_cam_matrix)
            self.r_cam_matrix = self._set_uri(req_user, r_cam_matrix)
            self.l_dist_coeffs = self._set_uri(req_user, l_dist_coeffs)
            self.r_dist_coeffs = self._set_uri(req_user, r_dist_coeffs)
            self.rt_cam_a2_cam_b = self._set_uri(req_user, rt_cam_a2_cam_b)
            self.stereo_E = self._set_uri(req_user, stereo_e)
            self.stereo_F = self._set_uri(req_user, stereo_f)
            self.stereo_R = self._set_uri(req_user, stereo_r)
            self.pixel_err = pixel_err

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

    @classmethod
    def to_obj(cls, args_dict, req_user=None):
        for k in StereoCalibration.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_stereo = StereoCalibration(args_dict[StereoCalibration.l_camera_id.name],
                                       args_dict[StereoCalibration.r_camera_id.name],
                                       args_dict[StereoCalibration.l_cam_matrix.name],
                                       args_dict[StereoCalibration.r_cam_matrix.name],
                                       args_dict[StereoCalibration.l_dist_coeffs.name],
                                       args_dict[StereoCalibration.r_dist_coeffs.name],
                                       args_dict[StereoCalibration.rt_cam_a2_cam_b.name],
                                       args_dict[StereoCalibration.stereo_E.name],
                                       args_dict[StereoCalibration.stereo_F.name],
                                       args_dict[StereoCalibration.stereo_R.name],
                                       args_dict[StereoCalibration.pixel_err.name],
                                       req_user
                                       )
        return new_stereo
