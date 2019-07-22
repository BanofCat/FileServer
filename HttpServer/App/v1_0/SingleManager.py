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
    def get(self, id):
        # get specify SingleCalibration by id
        self.logger.info('%s: get' % __name__)
        return self.get_base(SingleCalibration, id)

    # add new SingleCalibration or delete one by id
    # @AuthManager.user_auth
    def post(self):
        self.logger.info("%s: post" % __name__)
        try:
            if GENERA_ID_N not in self.req_dict:
                return self.make_http_response(False, 'you should set generate data table before you add this')
            req_obj = SingleCalibration.to_obj(self.req_dict[OBJECT_DATA_N])
            if SingleCalibration.is_exist(req_obj):
                return self.make_http_response(False, 'SingleCalibration is exist, can not add any more!')
            SingleCalibration.add(req_obj)
        except ObjectNotExist as e:
            self.logger.error(e.what())
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add SingleCalibration Success!')

    def put(self, loc_id):
        self.logger.info("%s: put" % __name__)
        self.logger.info("id: %d" % loc_id)
        location_obj = LocationList.get_by_id(loc_id)
        print(LocationList.to_dict(location_obj))
        req_ste = SingleCalibration.update_obj(self.req_dict[OBJECT_DATA_N], location_obj)
        if req_ste is None:
            return self.make_http_response(False, 'camera update data invalid')
        SingleCalibration.add(req_ste)
        return self.make_http_response(True, 'update success')

    def delete(self, id):
        self.logger.info('%s: delete' % __name__)
        ste_obj = SingleCalibration.get_by_id(id)
        if ste_obj is None:
            return self.make_http_response(False, 'delete stereo data not exist')
        obj_list = LocationList.query().filter(LocationList.single_ca_id == id).all()
        # remove all Location item's single id link
        for obj in obj_list:
            obj.stereo_ca_id = None
            LocationList.add(obj)
        return self.delete_base(SingleCalibration, id)
