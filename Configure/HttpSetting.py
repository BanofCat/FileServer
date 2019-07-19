# -*- coding:utf-8 -*-
import os

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





# user id name
USER_ID_N = 'user_id'
USER_ACCOUNT_N = 'user_account'
USER_NICKNAME_N = 'user_nickname'


LOGIN_STATE_N = 'is_login'

CAMERA_ID_N = 'id'

ROBOT_ID_N = 'id'

STEREO_ID_N = 'id'

SINGLE_ID_N = 'id'

REQ_ID_N = 'id'



# file manager
configure_path = os.path.realpath(__file__)
project_path = configure_path.rsplit('/', 2)[0]
UPLOAD_FOLDER = str(project_path) + '/HttpServer/Upload/'
print('UPLOAD_FOLDER: %s' % UPLOAD_FOLDER)


# server info

HTTP_HOST = '127.0.0.1'
HTTP_PORT = 8889
UPLOAD_END_POINT = 'upload'
DOWNLOAD_END_POINT = 'download'
UPLOAD_ROOT_URI = 'http://%s:%d/v1_0/%s/' % (HTTP_HOST, HTTP_PORT, UPLOAD_END_POINT)
DOWNLOAD_ROOT_URI = 'http://%s:%d/v1_0/%s/' % (HTTP_HOST, HTTP_PORT, DOWNLOAD_END_POINT)


# logger

HTTP_LOGGER_NAME = 'http_logger'
LOG_CONFIG_FILE = str(project_path) + '/Configure/logging.conf'


# stereo

GENERA_ID_N = 'generate_id'
