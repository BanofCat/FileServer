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
                 found_mask=None, img_pts=None, img_size=None, obj_pts=None, location_obj=None):

        BaseObject.__init__(self)
        self.set_location(location_obj)
        self._set_data(camera_id, n_camera_args, p_camera_args, n_distortion_args, p_distortion_args, n_toc,
                       p_toc, n_projection_err, p_projection_err, found_mask, img_pts, img_size, obj_pts)

    def _set_data(self, camera_id, n_camera_args=None, p_camera_args=None, n_distortion_args=None,
                  p_distortion_args=None, n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None,
                  found_mask=None, img_pts=None, img_size=None, obj_pts=None):

        self.set_cam(camera_id)
        self.n_camera_args = self.to_uri(n_camera_args)
        self.p_camera_args = self.to_uri(p_camera_args)
        self.n_distortion_args = self.to_uri(n_distortion_args)
        self.p_distortion_args = self.to_uri(p_distortion_args)
        self.n_toc = self.to_uri(n_toc)
        self.p_toc = self.to_uri(p_toc)
        self.n_projection_err = n_projection_err
        self.p_projection_err = p_projection_err
        self.found_mask = self.to_uri(found_mask)
        self.img_pts = self.to_uri(img_pts)
        self.set_size(img_size)
        self.obj_pts = self.to_uri(obj_pts)

    def to_uri(self, filename):
        if filename is None:
            return None
        abs_path = self.location_obj.get_upload_path() + self.__class__.__name__ + '/' + filename
        if not os.path.exists(abs_path):
            print('set uri failed: ', abs_path)
            raise ObjectNotExist("%s file is not exist, please upload first" % filename)
        return DOWNLOAD_ROOT_URI + str(self.location_obj.id) + '/' + self.__class__.__name__ + '/' + filename

    def set_cam(self, cam_id):
        if not Camera.is_exist_id(cam_id):
            raise ObjectNotExist("camera is not exits which id is %s" % cam_id)
        self.camera_id = cam_id

    def set_size(self, size_arr):
        self.img_size = str(size_arr)

    def set_location(self, loc_obj):
        self.location_obj = loc_obj

    @classmethod
    def to_obj(cls, args_dict, location_obj):
        if location_obj is None:
            raise ObjectNotExist('Location id is wrong')
        for k in SingleCalibration.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_single = SingleCalibration(args_dict[SingleCalibration.camera_id.name],
                                       args_dict[SingleCalibration.n_camera_args.name],
                                       args_dict[SingleCalibration.p_camera_args.name],
                                       args_dict[SingleCalibration.n_distortion_args.name],
                                       args_dict[SingleCalibration.p_distortion_args.name],
                                       args_dict[SingleCalibration.n_toc.name],
                                       args_dict[SingleCalibration.p_toc.name],
                                       args_dict[SingleCalibration.n_projection_err.name],
                                       args_dict[SingleCalibration.p_projection_err.name],
                                       args_dict[SingleCalibration.found_mask.name],
                                       args_dict[SingleCalibration.img_pts.name],
                                       args_dict[SingleCalibration.img_size.name],
                                       args_dict[SingleCalibration.obj_pts.name],
                                       location_obj
                                       )
        return new_single

    @classmethod
    def update_obj(cls, args_dict, loc_obj):

        if SingleCalibration.id.name not in args_dict:
            raise ObjectNotExist('SingleCalibration id is wrong')
        sin = SingleCalibration.get_by_id(args_dict[SingleCalibration.id.name])
        if sin is None:
            raise ObjectNotExist('SingleCalibration id is wrong')
        sin.set_location(loc_obj)
        # add origin data which are not in req data
        for k in SingleCalibration.__table__.columns:
            if k.name in args_dict and args_dict[k.name] is not None:
                if k.name == cls.camera_id.name:
                    sin.set_cam(args_dict[k.name])
                elif k.name == cls.img_size.name:
                    sin.set_size(args_dict[k.name])
                elif k.name == cls.n_camera_args.name or        \
                     k.name == cls.p_camera_args.name or        \
                     k.name == cls.n_distortion_args.name or    \
                     k.name == cls.p_distortion_args.name or    \
                     k.name == cls.n_toc.name or                \
                     k.name == cls.p_toc.name or                \
                     k.name == cls.found_mask.name or           \
                     k.name == cls.img_pts.name or              \
                     k.name == cls.obj_pts.name:
                    setattr(sin, k.name, sin.to_uri(args_dict[k.name]))
                else:
                    setattr(sin, k.name, args_dict[k.name])
        return sin
