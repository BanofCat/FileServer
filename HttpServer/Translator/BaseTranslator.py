import abc
from flask_restful import Resource


class BaseTranslator(Resource):

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

