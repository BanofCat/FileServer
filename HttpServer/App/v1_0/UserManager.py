from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from flask import make_response, render_template
from SQLManager.RelationalTableObject.User import User
from SQLManager.Exception.SqlException import *


class Registrar(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        super(Registrar, self).__init__()

    def get(self):
        print("%s: get" % __name__)
        response = make_response(render_template('registrar.html'))
        response.headers['Content-Type'] = 'text/html'
        return response

    def post(self):
        print("%s: post" % __name__)
        args = self.req_data
        req_user = self.package2obj(User, args)
        print("end")
        if User.is_exist(req_user):
            return self.make_http_response(False, 'User is exist, can not register any more, maybe you want to login!')
        try:
            User.add(req_user)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Register Success!')








