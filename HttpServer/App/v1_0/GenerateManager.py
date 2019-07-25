from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.GenerateData import GenerateData
from Exception.SqlException import ObjectNotExist
from Configure.HttpSetting import *
from SQLManager.RelationalTableObject.LocationList import LocationList


class GenerateManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        super(GenerateManager, self).__init__()

    # get all GenerateData list or single GenerateData info by id
    def get(self, id=None):
        # get specify GenerateData by id
        self.logger.info('%s: get' % __name__)
        return self.get_base(GenerateData, id)

    # add new GenerateData or delete one by id
    def post(self, id=None):
        self.logger.info("%s: post" % __name__)
        try:
            if id is not None:
                return self.make_http_response(False, 'this request method need not id arg')
            if OBJECT_DATA_N not in self.req_dict:
                return self.make_http_response(False, 'request data is invalid')
            req_gen = GenerateData.to_obj(self.req_dict[OBJECT_DATA_N])
            if GenerateData.is_exist(req_gen):
                return self.make_http_response(False, 'GenerateData is exist, can not add any more!')
            GenerateData.add(req_gen)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add GenerateData Success!')

    def put(self, id=None):
        self.logger.info('%s: put' % __name__)
        try:
            if id is not None:
                return self.make_http_response(False, 'this request method need not id arg')
            if OBJECT_DATA_N not in self.req_dict:
                return self.make_http_response(False, 'request data is invalid')
            req_gen = GenerateData.update_obj(self.req_dict[OBJECT_DATA_N])
            if req_gen is None:
                return self.make_http_response(False, 'camera update data invalid')
            GenerateData.add(req_gen)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'update success')

    def delete(self, id=None):
        self.logger.info('%s: delete' % __name__)
        if id is None:
            return self.make_http_response(False, 'this request method need a id arg')
        ste_obj = GenerateData.get_by_id(id)
        if ste_obj is None:
            return self.make_http_response(False, 'delete stereo data not exist')
        obj_list = LocationList.query().filter(LocationList.g_id == id).all()

        # todo: LocationList.g_id can not be None
        # remove all Location item with generate data id link
        for obj in obj_list:
            LocationList.delete(obj)
        return self.delete_base(GenerateData, id)
