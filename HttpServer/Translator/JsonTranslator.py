from HttpServer.Translator.BaseTranslator import BaseTranslator
import json


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
    def obj2dict(cls, obj_class, obj):
        pass

    @classmethod
    def to_dict(cls, args):
        str_args = ""
        if isinstance(args, bytes):
            str_args = args.decode('ascii')
        elif isinstance(args, dict):
            str_args = dict(map(JsonTranslator.to_dict, args.items()))
        elif isinstance(args, tuple):
            str_args = map(JsonTranslator.convert, args)
        return json.loads(str_args)

