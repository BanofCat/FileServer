from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.Camera import Camera
from SQLManager.Exception.SqlException import *
from HttpServer.Configure.HttpSetting import *


class CameraManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        super(CameraManager, self).__init__()

    # get all camera list or single camera info by id
    def get(self):
        # get specify camera by id
        if CAMERA_ID_N in self.req_dict:
            req_cam = Camera.get_by_id(self.req_dict[CAMERA_ID_N])
            if req_cam is None:
                return self.make_http_response(False, 'Camera id not exist！')
            req_cam_dict = self.obj2package(Camera, req_cam)
            return self.make_http_response(True, 'camera %s info:' % req_cam.id, msg_obj=req_cam_dict)
        # get camera id list
        else:
            req_cam_list = Camera.get_all_gen_list()

            if req_cam_list is None:
                return self.make_http_response(False, 'Camera list is null, please add some first')
            req_cam_dict_list = self.obj2package_list(Camera, req_cam_list)
            return self.make_http_response(True, 'camera list', msg_obj=req_cam_dict_list)

    # add new camera or delete one by id
    def post(self):

        print("%s: post" % __name__)
        args = self.req_data
        req_cam = self.package2obj(Camera, args)
        print("end")
        if Camera.is_exist(req_cam):
            return self.make_http_response(False,
                                           'Camera is exist, can not add any more!')
        try:
            Camera.add(req_cam)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add Camera Success!')