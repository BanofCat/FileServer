# -*- coding:utf-8 -*-
from SQLManager import sql_object
from flask import Flask
from SQLManager.Configure import DB_Setting
from SQLManager.RelationalTableObject.user import User
from SQLManager.Configure.DB_Setting import DB_NAME


if __name__ == '__main__':

    print("test start")
    test_app = Flask(__name__)
    test_app.config.from_object(DB_Setting)  # connect to db driver
    sql_object.init_app(test_app)
    test_app.app_context().push()

    # # test_api = Api(test_app)
    # sql_object.create_engine(SQLALCHEMY_DATABASE_URI, None)
    sql_object.engine.execute('CREATE DATABASE IF NOT EXISTS %s' % DB_NAME)     # create db
    sql_object.engine.execute('USE %s' % DB_NAME)   # select db to use
    sql_object.create_all(app=test_app)

    test_user = User("test", "test", "TestHello", "qweqweaaa")
    test_user1 = User("test1", "test1", "TestHello1", "RR")
    User.add(test_user, True)
    User.add(test_user1, True)
    # # User.add(1)
    print("test end")
