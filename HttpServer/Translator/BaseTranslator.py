import abc
from flask_restful import Resource
import logging
import logging.config
from Configure.HttpSetting import HTTP_LOGGER_NAME, LOG_CONFIG_FILE


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

