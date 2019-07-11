import abc
from flask_restful import Resource, reqparse


class BaseTranslator(Resource):

    @abc.abstractmethod
    def obj2package(self, obj_class, obj):
        pass

    @abc.abstractmethod
    def package2obj(self, obj_class, package):
        pass

    @abc.abstractmethod
    def make_http_response(self, is_success, res_title, res_code=None, msg_obj=None):
        pass

