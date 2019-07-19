from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.SingleCalibration import SingleCalibration
from flask import session
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist
from HttpServer.App.v1_0.AuthManager import AuthManager


class SingleManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        self.user_id = session.get(USER_ID_N)
        super(SingleManager, self).__init__()

    # get all SingleCalibration list or single SingleCalibration info by id
    def get(self):
        # get specify SingleCalibration by id
        if SingleCalibration.__table__.columns.id.name in self.req_dict:
            req_obj = SingleCalibration.get_by_id(self.req_dict[SINGLE_ID_N])
            if req_obj is None:
                return self.make_http_response(False, 'SingleCalibration id not exist！')
            req_rob_dict = SingleManager.to_dict(req_obj)
            return self.make_http_response(True, 'SingleCalibration %s info:' % req_obj.id, msg_obj=req_rob_dict)
        # get SingleCalibration id list
        else:
            req_obj_list = SingleCalibration.get_all_gen_list()

            if req_obj_list is None:
                return self.make_http_response(False, 'SingleCalibration list is null, please add some first')
            req_rob_dict_list = SingleCalibration.to_dict(req_obj_list)
            return self.make_http_response(True, 'SingleCalibration list', msg_obj=req_rob_dict_list)

    # add new SingleCalibration or delete one by id
    @AuthManager.user_auth
    def post(self, req_user):
        self.logger.info("%s: post" % __name__)
        try:
            if GENERA_ID_N not in self.req_dict:
                return self.make_http_response(False, 'you should set generate data table before you add this')

            req_obj = SingleCalibration.to_obj(self.req_dict[OBJECT_DATA_N], req_user)
            if SingleCalibration.is_exist(req_obj):
                return self.make_http_response(False, 'SingleCalibration is exist, can not add any more!')
            SingleCalibration.add(req_obj)
        except ObjectNotExist as e:
            self.logger.error(e.what())
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add SingleCalibration Success!')
