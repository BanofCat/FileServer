from flask import session
from HttpServer.Configure.HttpSetting import USER_ID_N
from SQLManager.RelationalTableObject.User import User
from HttpServer.Translator.BaseTranslator import BaseTranslator



class AuthManager(object):

    login_id_list = []

    def __init__(self):
        self.user_id_n = USER_ID_N

    @classmethod
    def user_auth(cls, func):
        def wrapper(self, **kwargs):
            user_id = session[USER_ID_N]
            if not cls.is_login(user_id):
                return BaseTranslator.make_http_response(False, 'Please login first')
            login_user = User.get(user_id)
            ret_response = func(self, login_user, **kwargs)
            return ret_response
        return wrapper

    @classmethod
    def is_login(cls, id):
        if  id in cls.login_id_list:
            return True
        return False

    @classmethod
    def add_login(cls, id):
        if not User.is_exist_id(id):
            return False
        cls.login_id_list.append(id)
        return True

    @classmethod
    def del_login(cls, id):
        if id in cls.login_id_list:
            cls.login_id_list.remove(id)
        return True

    @classmethod
    def clear_login(cls):
        cls.login_id_list.clear()

    @classmethod
    def list_login(cls):
        return cls.login_id_list.copy()