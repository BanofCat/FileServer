from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.DH_Optimised import DH_Optimised
from flask import session
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist
from HttpServer.App.v1_0.AuthManager import AuthManager


class DH_OptimisedManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        self.user_id = session.get(USER_ID_N)
        super(DH_OptimisedManager, self).__init__()

    # get all DH_Optimised list or single DH_Optimised info by id
    def get(self):
        # get specify DH_Optimised by id
        if DH_Optimised.__table__.columns.id.name in self.req_dict:
            req_obj = DH_Optimised.get_by_id(self.req_dict[SINGLE_ID_N])
            if req_obj is None:
                return self.make_http_response(False, 'DH_Optimised id not exist！')
            req_rob_dict = DH_OptimisedManager.to_dict(req_obj)
            return self.make_http_response(True, 'DH_Optimised %s info:' % req_obj.id, msg_obj=req_rob_dict)
        # get DH_Optimised id list
        else:
            req_obj_list = DH_Optimised.get_all_gen_list()

            if req_obj_list is None:
                return self.make_http_response(False, 'DH_Optimised list is null, please add some first')
            req_rob_dict_list = DH_Optimised.to_dict(req_obj_list)
            return self.make_http_response(True, 'DH_Optimised list', msg_obj=req_rob_dict_list)

    # add new DH_Optimised or delete one by id
    @AuthManager.user_auth
    def post(self, req_user):
        self.logger.info("%s: post" % __name__)
        try:
            if GENERA_ID_N not in self.req_dict:
                return self.make_http_response(False, 'you should set generate data table before you add this')

            req_obj = DH_Optimised.to_obj(self.req_dict[OBJECT_DATA_N], req_user)
            if DH_Optimised.is_exist(req_obj):
                return self.make_http_response(False, 'DH_Optimised is exist, can not add any more!')
            DH_Optimised.add(req_obj)
        except ObjectNotExist as e:
            self.logger.error(e.what())
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add DH_Optimised Success!')
