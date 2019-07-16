# -*- coding:utf-8 -*-
import os
from datetime import timedelta

# 请求数据包key
REQ_MSG_BODY_NAME = 'req_msg'

#
OBJECT_DATA_N = 'obj_data'


# login/register key list
# 请求用户key
ACCOUNT_N = 'account'

# 请求密码key
PASSWORD_N = 'password'

# 请求密码确认key
PASSWORD_CONFIRM_N = 'password_confirm'

# 请求昵称key
NICKNAME_N = 'nickname'

# 24位随机字符， 每次服务器启动则session清除
SECRET_KEY = os.urandom(24)

# session保存时间
PERMANENT_SESSION_LIFETIME = timedelta(days=1)





# user id name
USER_ID_N = 'id'


LOGIN_STATE_N = 'is_login'

CAMERA_ID_N = 'id'

ROBOT_ID_N = 'id'

STEREO_ID_N = 'id'



# file manager
configure_path = os.path.realpath(__file__)
project_path = configure_path.rsplit('/', 2)[0]
UPLOAD_FOLDER = str(project_path) + '/Upload/'
print('UPLOAD_FOLDER: %s' % UPLOAD_FOLDER)


# server info

HTTP_HOST = '127.0.0.1'
HTTP_PORT = 8889
UPLOAD_END_POINT = 'upload'
UPLOAD_ROOT_URI = 'http://%s:%d/v1_0/%s/' % (HTTP_HOST, HTTP_PORT, UPLOAD_END_POINT)
