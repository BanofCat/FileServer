import abc
from flask_restful import Resource, reqparse


class BaseTranslator(Resource):

    @classmethod
    @abc.abstractmethod
    def obj2package(cls, obj):
        pass

    @classmethod
    @abc.abstractmethod
    def package2obj(cls, package):
        pass


