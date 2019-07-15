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

