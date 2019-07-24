from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.StereoCalibration import StereoCalibration
from flask import session
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist
from HttpServer.App.v1_0.AuthManager import AuthManager
from SQLManager.RelationalTableObject.LocationList import LocationList


class StereoManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        self.user_id = session.get(USER_ID_N)
        super(StereoManager, self).__init__()

    # get all StereoCalibration list or single StereoCalibration info by id
    def get(self, id=None):
        # get specify StereoCalibration by id
        self.logger.info('%s: get' % __name__)
        return self.get_base(StereoCalibration, id)

    # add new StereoCalibration or delete one by id
    # @AuthManager.user_auth
    def post(self, id):
        self.logger.info("%s: post" % __name__)
        if id is None:
            return self.make_http_response(False, 'need a location id, stereo data should be bind to a location item')
        try:
            location_obj = LocationList.get_by_id(id)
            if location_obj is None:
                raise ObjectNotExist('Location id is wrong')
            req_obj = StereoCalibration.to_obj(self.req_dict[OBJECT_DATA_N], location_obj)
            if StereoCalibration.is_exist(req_obj):
                return self.make_http_response(False, 'StereoCalibration is exist, can not add any more!')
            # commit the data , so id will refresh from database
            StereoCalibration.add(req_obj, True)
            location_obj.set_stereo_id(req_obj.id)
            LocationList.add(location_obj)
        except ObjectNotExist as e:
            self.logger.error(e.what())
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add StereoCalibration Success!')

    def put(self, id):
        self.logger.info("%s: put" % __name__)
        self.logger.info("id: %d" % id)
        try:
            location_obj = LocationList.get_by_id(id)
            print(LocationList.to_dict(location_obj))
            req_ste = StereoCalibration.update_obj(self.req_dict[OBJECT_DATA_N], location_obj)
            if req_ste is None:
                return self.make_http_response(False, 'camera update data invalid')
            StereoCalibration.add(req_ste)
        except ObjectNotExist as e:
            self.logger.error(e.what())
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'update success')

    def delete(self, id):
        self.logger.info('%s: delete' % __name__)
        ste_obj = StereoCalibration.get_by_id(id)
        if ste_obj is None:
            return self.make_http_response(False, 'delete stereo data not exist')
        obj_list = LocationList.query().filter(LocationList.stereo_ca_id == id).all()
        # remove all Location item's stereo id link
        for obj in obj_list:
            obj.stereo_ca_id = None
            LocationList.add(obj)
        return self.delete_base(StereoCalibration, id)

