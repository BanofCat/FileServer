# -*- coding:utf-8 -*-
from datetime import timedelta
import os
# 常见配置文件：即database url，创建数据库引擎需要
# MySQL-Python：mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
#
# pymysql：mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
#
# MySQL-Connector：mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>

# sqlite:///<path>/<dbname>
#
# cx_Oracle：oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]

DB_SERVER = 'mysql'
DB_DRIVER = 'pymysql'
DB_ACCOUNT = "ban"
DB_PASSWORD = "root"
DB_HOST = "127.0.0.1"
DB_PORT = "3306"
DB_NAME = "image_database_test"

# data base connect url
SQLALCHEMY_DATABASE_URI = "%s+%s://%s:%s@%s:%s/?charset=utf8" % (
    DB_SERVER, DB_DRIVER, DB_ACCOUNT, DB_PASSWORD, DB_HOST, DB_PORT
)
# SQLALCHEMY_DATABASE_URI = "%s+%s://%s:%s@%s:%s/%s?charset=utf8" % (
#     DB_SERVER, DB_DRIVER, DB_ACCOUNT, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
# )

SQLALCHEMY_TRACK_MODIFICATIONS = False
# file upload limit
ALLOW_EXTENSIONS = ('png', 'jpeg', 'svg', 'txt')

# 24位随机字符， 每次服务器启动则session清除
SECRET_KEY = os.urandom(24)

# session保存时间
PERMANENT_SESSION_LIFETIME = timedelta(days=1)

# logger
configure_path = os.path.realpath(__file__)
project_path = configure_path.rsplit('/', 2)[0]
DB_LOGGER_NAME = 'db_logger'
LOG_CONFIG_FILE = str(project_path) + '/Configure/logging.conf'