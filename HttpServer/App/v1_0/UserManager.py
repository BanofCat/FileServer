from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from flask import make_response, render_template
from SQLManager.RelationalTableObject.User import User
from HttpServer.App.v1_0.AuthManager import AuthManager
from flask import session
from HttpServer.Configure.HttpSetting import *


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
        req_user = User.to_obj(args)
        print("end")
        if User.is_exist(req_user):
            return self.make_http_response(False, 'User is exist, can not register any more, maybe you want to login!')
        try:
            User.add(req_user)
        except ObjectNotExist as e:
            return self.make_http_response(False, e.what())
        return self.make_http_response(True, 'Register Success!')


class Login(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        super(Login, self).__init__()

    def post(self):
        print("%s: post" % __name__)
        args_dict = self.to_dict(self.req_data)
        print('>>>>', args_dict)
        if LOGIN_STATE_N in args_dict.keys() and args_dict[LOGIN_STATE_N] is True:    # login
            req_user = User.get_by_account(args_dict[ACCOUNT_N])
            if req_user is None or not req_user.check_password(args_dict[PASSWORD_N]):
                return self.make_http_response(False, "Account is not match password!")
            AuthManager.add_login(req_user.id)
            session[USER_ID_N] = req_user.id    # record the login id to session
            return self.make_http_response(True, "Login Success!")
        else:       # logout

            AuthManager.del_login(session.get(USER_ID_N))
            return self.make_http_response(True, "Logout Success!")












