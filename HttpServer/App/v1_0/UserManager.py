from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from flask import make_response, render_template
from SQLManager.RelationalTableObject.User import User
from flask import session
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist


class Registrar(JsonTranslator):

    def __init__(self):
        self.req_data = reqparse.request.data
        super(Registrar, self).__init__()

    def get(self):
        self.logger.info("%s: get" % __name__)
        response = make_response(render_template('registrar.html'))
        response.headers['Content-Type'] = 'text/html'
        return response

    def post(self):
        self.logger.info("%s: post" % __name__)
        args = self.req_data
        req_user = User.to_obj(args)
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
        self.logger.info("%s: post" % __name__)
        args_dict = self.to_dict(self.req_data)
        if session.get(USER_ID_N) is not None:
            return self.make_http_response(False, 'You has been login, need not to do it again')
        if LOGIN_STATE_N in args_dict.keys() and args_dict[LOGIN_STATE_N] is True:    # login
            req_user = User.get_by_account(args_dict[ACCOUNT_N])
            if req_user is None or not req_user.check_password(args_dict[PASSWORD_N]):
                return self.make_http_response(False, "Account is not match password!")
            session[USER_ID_N] = req_user.id    # record the login id to session
            session[USER_ACCOUNT_N] = req_user.account
            session[USER_NICKNAME_N] = req_user.nickname
            self.logger.info('login id: ', session.get(USER_ID_N))
            return self.make_http_response(True, "Login Success, Hello %s!" % req_user.nickname)
        else:       # logout
            user_nickname = session.get(USER_NICKNAME_N)
            session.pop(USER_ID_N, None)    # delete login id in session
            session.pop(USER_ACCOUNT_N, None)    # delete login id in session
            session.pop(USER_NICKNAME_N, None)    # delete login id in session

            return self.make_http_response(True, "Good Bye %s!" % user_nickname)












