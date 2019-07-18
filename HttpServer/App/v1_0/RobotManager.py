from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.Robot import Robot


class RobotManager(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        super(RobotManager, self).__init__()

    # get all Robot list or single Robot info by id
    def get(self):
        # get specify Robot by id
        if ROBOT_ID_N in self.req_dict:
            req_rob = Robot.get_by_id(self.req_dict[ROBOT_ID_N])
            if req_rob is None:
                return self.make_http_response(False, 'Robot id not exist！')
            req_rob_dict = self.obj2package(Robot, req_rob)
            return self.make_http_response(True, 'Robot %s info:' % req_rob.id, msg_obj=req_rob_dict)
        # get Robot id list
        else:
            req_rob_list = Robot.get_all_gen_list()

            if req_rob_list is None:
                return self.make_http_response(False, 'Robot list is null, please add some first')
            req_rob_dict_list = self.obj2package_list(Robot, req_rob_list)
            return self.make_http_response(True, 'Robot list', msg_obj=req_rob_dict_list)

    # add new Robot or delete one by id
    def post(self):

        self.logger.info("%s: post" % __name__)
        args = self.req_data
        req_rob = self.package2obj(Robot, args)
        if Robot.is_exist(req_rob):
            return self.make_http_response(False,
                                           'Robot is exist, can not add any more!')
        try:
            Robot.add(req_rob)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Add Robot Success!')
