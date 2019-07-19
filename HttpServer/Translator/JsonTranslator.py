from HttpServer.Translator.BaseTranslator import BaseTranslator
import json
import abc
from Configure.HttpSetting import *

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


        # # get specify camera by id
        # if CAMERA_ID_N in self.req_dict:
        #     req_cam = Camera.get_by_id(self.req_dict[CAMERA_ID_N])
        #     if req_cam is None:
        #         return self.make_http_response(False, 'Camera id not exist！')
        #     req_cam_dict = Camera.to_dict(req_cam)
        #     return self.make_http_response(True, 'camera %s info:' % req_cam.id, msg_obj=req_cam_dict)
        # # get camera id list
        # else:
        #     req_cam_list = Camera.get_all_gen_list()
        #     if req_cam_list is None:
        #         return self.make_http_response(False, 'Camera list is null, please add some first')
        #     req_cam_dict_list = Camera.to_dict(req_cam_list)
        #     return self.make_http_response(True, 'camera list', msg_obj=req_cam_dict_list)

