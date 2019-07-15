from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.StereoCalibration import StereoCalibration
from SQLManager.Exception.SqlException import *
from HttpServer.Configure.HttpSetting import *


class StereoManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        super(StereoManager, self).__init__()

    # get all StereoCalibration list or single StereoCalibration info by id
    def get(self):
        # get specify StereoCalibration by id
        if STEREO_ID_N in self.req_dict:
            req_rob = StereoCalibration.get_by_id(self.req_dict[STEREO_ID_N])
            if req_rob is None:
                return self.make_http_response(False, 'StereoCalibration id not exist！')
            req_rob_dict = self.obj2package(StereoCalibration, req_rob)
            return self.make_http_response(True, 'StereoCalibration %s info:' % req_rob.id, msg_obj=req_rob_dict)
        # get StereoCalibration id list
        else:
            req_rob_list = StereoCalibration.get_all_gen_list()

            if req_rob_list is None:
                return self.make_http_response(False, 'StereoCalibration list is null, please add some first')
            req_rob_dict_list = self.obj2package_list(StereoCalibration, req_rob_list)
            return self.make_http_response(True, 'StereoCalibration list', msg_obj=req_rob_dict_list)

    # add new StereoCalibration or delete one by id
    def post(self):

        print("%s: post" % __name__)
        req_rob = StereoCalibration(self.req_dict[OBJECT_DATA_N])
        print("end")
        if StereoCalibration.is_exist(req_rob):
            return self.make_http_response(False, 'StereoCalibration is exist, can not add any more!')
        try:
            StereoCalibration.add(req_rob)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add StereoCalibration Success!')
