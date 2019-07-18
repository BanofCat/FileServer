# -*- coding:utf-8 -*-
from SQLManager import sql_object
from flask import Flask
from Configure import DB_Setting
from SQLManager.RelationalTableObject.User import User
from SQLManager.RelationalTableObject.Camera import Camera
from SQLManager.RelationalTableObject.Robot import Robot
from SQLManager.RelationalTableObject.DH_Optimised import DH_Optimised
from SQLManager.RelationalTableObject.GenerateData import GenerateData
from SQLManager.RelationalTableObject.InverseTest import InverseTest
from SQLManager.RelationalTableObject.LocationList import LocationList
from SQLManager.RelationalTableObject.SingleCalibration import SingleCalibration
from SQLManager.RelationalTableObject.StereoCalibration import StereoCalibration
from SQLManager.RelationalTableObject.DH_Optimised import DH_Model
from Configure import DB_NAME

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
    try:

        test_user = User("test1", "test1", "TestHello5")
        test_user1 = User("test2", "test2", "TestHello6")
        test_camera = Camera("test3", "test3", "TestHello7")
        test_robot = Robot("test4", 4, "RR")
        test_gen = GenerateData("test4", 1)

        Camera.add(test_camera)
        Robot.add(test_robot)
        User.add(test_user1)
        User.add(test_user, True)
        GenerateData.add(test_gen, True)

        test_single = SingleCalibration("test3")
        test_stereo = StereoCalibration("test3", "test3")
        test_dh = DH_Optimised(DH_Model.Faset)
        test_inv = InverseTest()
        test_loc = LocationList(1)
        SingleCalibration.add(test_single)
        StereoCalibration.add(test_stereo)
        DH_Optimised.add(test_dh)
        InverseTest.add(test_inv)
        LocationList.add(test_loc, True)
    except ObjectNotExist as e:
        print(e.what())
    # # User.add(1)
    print("test end")
