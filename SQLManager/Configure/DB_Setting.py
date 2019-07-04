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


DB_ACCOUNT = "Ban"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_PORT = "12345"
DB_NAME = "image_database"

# data base connect url
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utr8" % (DB_ACCOUNT, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

# file upload limit
ALLOW_EXTENSIONS = ('png', 'jpeg', 'svg')
