from flask import session
from Configure.HttpSetting import USER_ID_N
from SQLManager.RelationalTableObject.User import User
from HttpServer.Translator.JsonTranslator import JsonTranslator


class AuthManager(object):

    def __init__(self):
        pass

    @classmethod
    def user_auth(cls, func):
        print('%s: user_auth' % __name__)

        def wrapper(self, **kwargs):
            user_id = session.get(USER_ID_N)
            if user_id is None:
                print('Please login first')
                return JsonTranslator.make_http_response(False, 'Please login first')
            login_user = User.get_by_id(user_id)
            ret_response = func(self, login_user, **kwargs)
            return ret_response
        return wrapper

