from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.Camera import Camera
from Exception.SqlException import ObjectNotExist
from Configure.HttpSetting import *
from SQLManager.RelationalTableObject.LocationList import LocationList


class CameraManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        # self.user_id = session.get(USER_ID_N)
        super(CameraManager, self).__init__()

    # get all camera list or single camera info by id
    def get(self, id=None):
        self.logger.info('%s: get' % __name__)
        return self.get_base(Camera, id)

    # add new camera
    def post(self):

        self.logger.info("%s: post" % __name__)
        req_cam = Camera.to_obj(self.req_dict[OBJECT_DATA_N])
        if Camera.is_exist(req_cam):
            return self.make_http_response(False, 'Camera is exist, can not add any more!')
        try:
            Camera.add(req_cam)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add Camera Success!')

    # update camera data
    def put(self):
        pass

    # delete camera item
    def delete(self):
        pass
