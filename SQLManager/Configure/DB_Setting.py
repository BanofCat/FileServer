# -*- coding:utf-8 -*-

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
DB_ACCOUNT = "root"
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
