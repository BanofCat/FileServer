from HttpServer.Translator.BaseTranslator import BaseTranslator
import json
import decimal
from datetime import datetime, date
from sqlalchemy.orm.dynamic import AppenderQuery
from flask_sqlalchemy import BaseQuery, DeclarativeMeta
from SQLManager import sql_object
from SQLManager.RelationalTableObject.User import User
from HttpServer.Configure.HttpSetting import *


class JsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            fields = {}
            counter = 0
            for field in [x for x in dir(o) if not x.startswith('_') and x != 'metadata']:
                data = o.__getattribute__(field)
                counter += 1
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:

                    if isinstance(data, datetime):
                        fields[field] = data.strftime("%Y-%m-%d %H:%M:%S.%F")[:-3]
                    elif isinstance(data, date):
                        fields[field] = data.strftime("%Y-%m-%d")
                    elif isinstance(data, decimal.Decimal):
                        fields[field] = float(data)
                    elif isinstance(data, BaseQuery):
                        pass
                    elif isinstance(data, AppenderQuery):
                        pass
                    elif isinstance(data, type):
                        pass
                    elif isinstance(data, type(JsonEncoder.default)):
                        pass
                    elif isinstance(data, sql_object.Model):
                        pass
                    else:
                        fields[field] = JsonEncoder.default(self, data)
            return fields
        return json.JSONEncoder.default(self, o)


class JsonTranslator(BaseTranslator):

    response = {
        'req_state' : False,
        'title'     : '',
        'res_code'  : '',
        'res_msg'   : ''
    }

    @classmethod
    def make_http_response(cls, is_success, res_title, res_code=None, msg_obj=None):
        http_response = cls.response.copy()
        http_response['req_state'] = is_success
        http_response['title'] = res_title
        http_response['res_code'] = res_code
        http_response['res_msg'] = msg_obj
        return http_response

    @classmethod
    def obj2package(cls, obj_class, obj):
        pass

    @classmethod
    def package2obj(cls, obj_class, package):
        dict_package = eval(package)
        print(">>>>>>", dict_package)
        # if isinstance(obj_class, User):
        req_msg = dict_package[OBJECT_DATA_N]
        new_obj = User(req_msg[ACCOUNT_N], req_msg[PASSWORD_N], req_msg[NICKNAME_N])
        print(new_obj.id, new_obj.account, new_obj.password, new_obj.nickname)
        return new_obj

    @classmethod
    def to_dict(cls, args):
        return eval(args)

