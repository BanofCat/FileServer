from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.GenerateData import GenerateData
from SQLManager.Exception.SqlException import *
from HttpServer.Configure.HttpSetting import *


class GenerateManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        super(GenerateManager, self).__init__()

    # get all GenerateData list or single GenerateData info by id
    def get(self):
        # get specify camera by id
        if CAMERA_ID_N in self.req_dict:
            req_cam = GenerateData.get_by_id(self.req_dict[CAMERA_ID_N])
            if req_cam is None:
                return self.make_http_response(False, 'GenerateData id not exist！')
            req_cam_dict = self.obj2package(GenerateData, req_cam)
            return self.make_http_response(True, 'GenerateData %s info:' % req_cam.id, msg_obj=req_cam_dict)
        # get GenerateData id list
        else:
            req_cam_list = GenerateData.get_all_gen_list()

            if req_cam_list is None:
                return self.make_http_response(False, 'GenerateData list is null, please add some first')
            req_cam_dict_list = self.obj2package_list(GenerateData, req_cam_list)
            return self.make_http_response(True, 'GenerateData list', msg_obj=req_cam_dict_list)

    # add new GenerateData or delete one by id
    def post(self):

        print("%s: post" % __name__)
        args = self.req_data
        req_cam = self.package2obj(GenerateData, args)
        print("end")
        if GenerateData.is_exist(req_cam):
            return self.make_http_response(False, 'GenerateData is exist, can not add any more!')
        try:
            GenerateData.add(req_cam)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add GenerateData Success!')