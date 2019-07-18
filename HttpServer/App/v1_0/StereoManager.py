from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.StereoCalibration import StereoCalibration
from flask import session
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist
from HttpServer.App.v1_0.AuthManager import AuthManager


class StereoManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        self.user_id = session.get(USER_ID_N)
        super(StereoManager, self).__init__()

    # get all StereoCalibration list or single StereoCalibration info by id
    def get(self):
        # get specify StereoCalibration by id
        if StereoCalibration.__table__.columns.id.name in self.req_dict:
            req_obj = StereoCalibration.get_by_id(self.req_dict[STEREO_ID_N])
            if req_obj is None:
                return self.make_http_response(False, 'StereoCalibration id not exist！')
            req_rob_dict = StereoManager.to_dict(req_obj)
            return self.make_http_response(True, 'StereoCalibration %s info:' % req_obj.id, msg_obj=req_rob_dict)
        # get StereoCalibration id list
        else:
            req_obj_list = StereoCalibration.get_all_gen_list()

            if req_obj_list is None:
                return self.make_http_response(False, 'StereoCalibration list is null, please add some first')
            req_rob_dict_list = StereoCalibration.to_dict(req_obj_list)
            return self.make_http_response(True, 'StereoCalibration list', msg_obj=req_rob_dict_list)

    # add new StereoCalibration or delete one by id
    @AuthManager.user_auth
    def post(self, req_user):
        self.logger.info("%s: post" % __name__)
        try:
            if GENERA_ID_N not in self.req_dict:
                return self.make_http_response(False, 'you should set generate data table before you add this')

            req_obj = StereoCalibration.to_obj(self.req_dict[OBJECT_DATA_N], req_user)
            if StereoCalibration.is_exist(req_obj):
                return self.make_http_response(False, 'StereoCalibration is exist, can not add any more!')
            StereoCalibration.add(req_obj)
        except ObjectNotExist as e:
            self.logger.error(e.what())
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add StereoCalibration Success!')
