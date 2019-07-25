import abc
from flask_restful import Resource
import logging
import logging.config
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist
from Exception.SqlException import DBException


class BaseTranslator(Resource):

    def __init__(self):
        logging.config.fileConfig(LOG_CONFIG_FILE)
        self.logger = logging.getLogger(HTTP_LOGGER_NAME)
        self.logger.setLevel(logging.INFO)


    @abc.abstractmethod
    def obj2package(self, obj_class, obj):
        pass

    @abc.abstractmethod
    def package2obj(self, obj_class, package):
        pass

    @classmethod
    @abc.abstractmethod
    def make_http_response(cls, is_success, res_title, res_code=None, msg_obj=None):
        pass

    @classmethod
    @abc.abstractmethod
    def to_dict(cls, args):
        pass

    @abc.abstractmethod
    def get_base(self, obj_class, id=None):
        # get specify item by id
        if id is not None:
            print('id is', id)
            req_obj = obj_class.get_by_id(id)
            if req_obj is None:
                return self.make_http_response(False, '%s id not exist' % obj_class.__name__)
            req_rob_dict = obj_class.to_dict(req_obj)
            return self.make_http_response(True, '%s %s info' % (obj_class.__name__, req_obj.id), msg_obj=req_rob_dict)
        # get item id list
        else:
            req_obj_list = obj_class.get_all_gen_list()

            if req_obj_list is None:
                return self.make_http_response(False, '%s list is null, please add some first' % obj_class.__name__)
            req_rob_dict_list = obj_class.to_dict(req_obj_list)
            return self.make_http_response(True, '%s list' % obj_class.__name__, msg_obj=req_rob_dict_list)

    # delete item
    @abc.abstractmethod
    def delete_base(self, obj_class, id):
        try:
            obj = obj_class.get_by_id(id)
            if obj is not None:
                if not obj_class.delete(obj, True):
                    return self.make_http_response(False, 'delete failed, maybe delete item is a dependency')
            else:
                raise DBException
        except DBException as e:
            return self.make_http_response(False, 'delete id is not exist')
        return self.make_http_response(True, 'delete success', msg_obj=obj_class.to_dict(obj))
    # @abc.abstractmethod
    # def post(self, obj_class, id=None, obj_data=None):
    #     # add new item
    #     if id is None:
    #         req_cam = obj_class.to_obj(obj_data)
    #         if obj_class.is_exist(req_cam):
    #             return self.make_http_response(False, '%s is exist, can not add any more!' % obj_class.__name__)
    #         try:
    #             obj_class.add(req_cam)
    #         except ObjectNotExist as e:
    #             return self.make_http_response(False, e.what())
    #         return self.make_http_response(True, 'Add %s Success!' % obj_class.__name__)
    #
    #     # edit an exist item
    #     else:
    #         pass


