from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.Camera import Camera
from Configure.HttpSetting import *
from Exception.SqlException import *


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
    def post(self, id=None):
        self.logger.info("%s: post" % __name__)
        if id is not None:
            return self.make_http_response(False, 'this request method need not id arg')
        if OBJECT_DATA_N not in self.req_dict:
            return self.make_http_response(False, 'request data is invalid')
        req_cam = Camera.to_obj(self.req_dict[OBJECT_DATA_N])
        if Camera.is_exist(req_cam):
            return self.make_http_response(False, 'Camera is exist, can not add any more!')
        try:
            Camera.add(req_cam)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())

        return self.make_http_response(True, 'Add Camera Success!', msg_obj=Camera.to_dict(req_cam))

    # update camera data
    def put(self, id=None):
        self.logger.info("%s: put" % __name__)
        if id is not None:
            return self.make_http_response(False, 'this request method need not id arg')
        if OBJECT_DATA_N not in self.req_dict:
            return self.make_http_response(False, 'request data is invalid')
        req_cam = Camera.update_obj(self.req_dict[OBJECT_DATA_N])
        if req_cam is None:
            return self.make_http_response(False, 'camera update data invalid')
        print(req_cam.use_type)
        Camera.add(req_cam, True)
        return self.make_http_response(True, 'update success', msg_obj=Camera.to_dict(req_cam))

    # delete camera item
    def delete(self, id=None):
        if id is None:
            return self.make_http_response(False, 'need a id arg in url to delete object')
        self.logger.info('%s: delete' % __name__)
        return self.delete_base(Camera, id)


