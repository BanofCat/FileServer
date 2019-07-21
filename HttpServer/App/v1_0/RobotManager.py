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
    def get(self, id):
        self.logger.info('%s: get' % __name__)
        return self.get_base(Robot, id)
        # get specify Robot by id
        # if ROBOT_ID_N in self.req_dict:
        #     req_rob = Robot.get_by_id(self.req_dict[ROBOT_ID_N])
        #     if req_rob is None:
        #         return self.make_http_response(False, 'Robot id not exist！')
        #     req_rob_dict = self.obj2package(Robot, req_rob)
        #     return self.make_http_response(True, 'Robot %s info:' % req_rob.id, msg_obj=req_rob_dict)
        # # get Robot id list
        # else:
        #     req_rob_list = Robot.get_all_gen_list()
        #
        #     if req_rob_list is None:
        #         return self.make_http_response(False, 'Robot list is null, please add some first')
        #     req_rob_dict_list = self.obj2package_list(Robot, req_rob_list)
        #     return self.make_http_response(True, 'Robot list', msg_obj=req_rob_dict_list)

    # add new Robot or delete one by id
    def post(self):

        self.logger.info("%s: post" % __name__)
        req_cam = Robot.to_obj(self.req_dict[OBJECT_DATA_N])
        if Robot.is_exist(req_cam):
            return self.make_http_response(False, 'Robot is exist, can not add any more!')
        try:
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

    # delete Robot item
    def delete(self, id):
        self.logger.info('%s: delete' % __name__)
        try:
            Robot.delete(id)
        except DBException as e:
            return self.make_http_response(False, 'delete id is not exist')
        return self.make_http_response(True, 'delete success')

