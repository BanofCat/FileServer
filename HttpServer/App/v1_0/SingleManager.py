from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.SingleCalibration import SingleCalibration
from flask import session
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist
from HttpServer.App.v1_0.AuthManager import AuthManager
from SQLManager.RelationalTableObject.LocationList import LocationList


class SingleManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        self.user_id = session.get(USER_ID_N)
        super(SingleManager, self).__init__()

    # get all SingleCalibration list or single SingleCalibration info by id
    def get(self, id=None):
        # get specify SingleCalibration by id
        self.logger.info('%s: get' % __name__)
        return self.get_base(SingleCalibration, id)

    # add new SingleCalibration or delete one by id
    # @AuthManager.user_auth
    def post(self, id=None):
        self.logger.info("%s: post" % __name__)
        if id is None:
            return self.make_http_response(False, 'need a location id, single data should be bind to a location item')
        try:
            location_obj = LocationList.get_by_id(id)
            if location_obj is None:
                raise ObjectNotExist('Location id is wrong')
            if OBJECT_DATA_N not in self.req_dict:
                return self.make_http_response(False, 'request data is invalid')
            req_obj = SingleCalibration.to_obj(self.req_dict[OBJECT_DATA_N], location_obj)
            if SingleCalibration.is_exist(req_obj):
                return self.make_http_response(False, 'SingleCalibration is exist, can not add any more!')
            # commit the data , so id will refresh from database
            SingleCalibration.add(req_obj, True)
            location_obj.set_single_id(req_obj.id)
            LocationList.add(location_obj)
        except ObjectNotExist as e:
            self.logger.error(e.what())
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add SingleCalibration Success!')

    def put(self, id=None):
        self.logger.info("%s: put" % __name__)
        try:
            if id is None:
                return self.make_http_response(False, 'need a id arg')
            loc_obj = LocationList.get_by_id(id)
            if loc_obj is None:
                return self.make_http_response(False, 'Location obj is not exist which id is %s' % str(id))
            if OBJECT_DATA_N not in self.req_dict:
                return self.make_http_response(False, 'request data is invalid')
            req_ste = SingleCalibration.update_obj(self.req_dict[OBJECT_DATA_N], loc_obj)
            if req_ste is None:
                return self.make_http_response(False, 'camera update data invalid')
            SingleCalibration.add(req_ste)
        except ObjectNotExist as e:
            self.logger.error(e.what())
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'update success')

    def delete(self, id=None):
        self.logger.info('%s: delete' % __name__)
        if id is None:
            return self.make_http_response(False, 'need a id arg')
        ste_obj = SingleCalibration.get_by_id(id)
        if ste_obj is None:
            return self.make_http_response(False, 'delete stereo data not exist')
        obj_list = LocationList.query().filter(LocationList.single_ca_id == id).all()
        # remove all Location item's single id link
        for obj in obj_list:
            obj.stereo_ca_id = None
            LocationList.add(obj)
        return self.delete_base(SingleCalibration, id)
