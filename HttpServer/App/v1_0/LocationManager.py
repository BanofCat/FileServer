from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.LocationList import LocationList
from Configure.HttpSetting import *
from Exception.SqlException import *


class LocationManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        # self.user_id = session.get(USER_ID_N)
        super(LocationManager, self).__init__()

    # get all LocationList list or single LocationList info by id
    def get(self, id=None):
        self.logger.info('%s: get' % __name__)
        return self.get_base(LocationList, id)

    # add new LocationList
    def post(self, id=None):

        self.logger.info("%s: post" % __name__)
        try:
            if id is not None:
                return self.make_http_response(False, 'need not a id arg')
            if OBJECT_DATA_N not in self.req_dict:
                return self.make_http_response(False, 'request data is invalid')
            req_loc = LocationList.to_obj(self.req_dict[OBJECT_DATA_N])
            if LocationList.is_exist(req_loc):
                return self.make_http_response(False, 'LocationList is exist, can not add any more!')
            LocationList.add(req_loc)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add LocationList Success!')

    # update LocationList data
    def put(self, id=None):
        self.logger.info("%s: put" % __name__)
        try:
            if id is not None:
                return self.make_http_response(False, 'need not a id arg')
            if OBJECT_DATA_N not in self.req_dict:
                return self.make_http_response(False, 'request data is invalid')
            req_loc = LocationList.update_obj(self.req_dict[OBJECT_DATA_N])
            if req_loc is None:
                return self.make_http_response(False, 'LocationList update data invalid')
            print(req_loc.use_type)
            LocationList.add(req_loc, True)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'update success')

    # delete LocationList item
    def delete(self, id=None):
        self.logger.info('%s: delete' % __name__)
        if id is not None:
            return self.make_http_response(False, 'need a id arg')
        try:
            LocationList.delete(id)
        except DBException as e:
            return self.make_http_response(False, 'delete id is not exist')
        return self.make_http_response(True, 'delete success')


