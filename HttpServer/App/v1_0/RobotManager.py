from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.Robot import Robot
from Configure.HttpSetting import *
from Exception.SqlException import *


class RobotManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        super(RobotManager, self).__init__()

    # get all Robot list or single Robot info by id
    def get(self, id=None):
        self.logger.info('%s: get' % __name__)
        return self.get_base(Robot, id)

    # add new Robot or delete one by id
    def post(self):
        self.logger.info("%s: post" % __name__)
        try:
            req_cam = Robot.to_obj(self.req_dict[OBJECT_DATA_N])
            if Robot.is_exist(req_cam):
                return self.make_http_response(False, 'Robot is exist, can not add any more!')
            Robot.add(req_cam)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add Robot Success!')

    # update Robot data
    def put(self):
        self.logger.info("%s: put" % __name__)
        req_cam = Robot.update_obj(self.req_dict[OBJECT_DATA_N])
        if req_cam is None:
            return self.make_http_response(False, 'Robot update data invalid')
        Robot.add(req_cam)
        return self.make_http_response(True, 'update success')

    # delete robot item
    def delete(self, id):
        self.logger.info('%s: delete' % __name__)
        return self.delete_base(Robot, id)

