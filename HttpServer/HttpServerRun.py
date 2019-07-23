#!/usr/bin/env python

from flask_restful import Api
from flask import Flask
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from Configure import DB_Setting
from Configure.DB_Setting import DB_NAME
from Configure.HttpSetting import *
from sqlalchemy.exc import SQLAlchemyError
import json

def url_init(api_obj):
    from HttpServer.App.v1_0.UserManager import Registrar, Login
    from HttpServer.App.v1_0.CameraManager import CameraManager
    from HttpServer.App.v1_0.FileManager import FileUpload, FileDownload
    from HttpServer.App.v1_0.StereoManager import StereoManager
    from HttpServer.App.v1_0.RobotManager import RobotManager
    from HttpServer.App.v1_0.GenerateManager import GenerateManager
    from HttpServer.App.v1_0.LocationManager import LocationManager
    from HttpServer.App.v1_0.SingleManager import SingleManager
    from HttpServer.App.v1_0.DH_OptimisedManger import DH_OptimisedManager
    from HttpServer.App.v1_0.InverseManager import InverseManager

    # register and login
    api_obj.add_resource(
        Registrar,
        '/v1_0/registrar/',
        endpoint='Registrar'
    )

    api_obj.add_resource(
        Login,
        '/v1_0/login/',
        endpoint='Login'
    )

    # camera
    api_obj.add_resource(
        CameraManager,
        '/v1_0/camera/<string:id>',
        endpoint='Camera'
    )

    api_obj.add_resource(
        CameraManager,
        '/v1_0/camera/',
        endpoint='CameraList'
    )

    # robot
    api_obj.add_resource(
        RobotManager,
        '/v1_0/robot/',
        endpoint='RobotList'
    )

    api_obj.add_resource(
        RobotManager,
        '/v1_0/robot/<string:id>',
        endpoint='Robot'
    )

    # file upload and download
    api_obj.add_resource(
        FileUpload,
        '/v1_0/%s/' % UPLOAD_END_POINT,
        endpoint='Upload'
    )

    api_obj.add_resource(
        FileDownload,
        '/v1_0/%s/<string:filename>' % DOWNLOAD_END_POINT,
        endpoint='Download'
    )

    # generate data
    api_obj.add_resource(
        GenerateManager,
        '/v1_0/generate/',
        endpoint='GenerateList'
    )
    api_obj.add_resource(
        GenerateManager,
        '/v1_0/generate/<int:id>',
        endpoint='Generate'
    )

    # location data
    api_obj.add_resource(
        LocationManager,
        '/v1_0/location/',
        endpoint='LocationList'
    )

    api_obj.add_resource(
        LocationManager,
        '/v1_0/location/<int:id>',
        endpoint='Location'
    )

    # single data
    api_obj.add_resource(
        SingleManager,
        '/v1_0/single/<int:loc_id>',
        endpoint='Single'
    )

    # stereo data
    api_obj.add_resource(
        StereoManager,
        '/v1_0/stereo/<int:loc_id>',
        endpoint='Stereo'
    )

    # dh data
    api_obj.add_resource(
        DH_OptimisedManager,
        '/v1_0/dh/<int:loc_id>',
        endpoint='DH'
    )

    # inverse data
    api_obj.add_resource(
        InverseManager,
        '/v1_0/inverse/<int:loc_id>',
        endpoint='Inverse'
    )



def create_app(configure_file):
    new_app = Flask(__name__)

    web_api = Api(new_app)

    url_init(web_api)

    new_app.config.from_object(configure_file)

    return new_app


web_app = create_app(DB_Setting)
web_app.app_context().push()


@web_app.after_request
def after_request(response):
    try:
        BaseObject.commit()
    except SQLAlchemyError as e:
        sql_object.session.rollback()
        response.json['req_state'] = False
        response.json['title'] = str(e)
        response.data = json.dumps(response.json)
        print('ret: ', response.data)
        return response
    return response

sql_object.init_app(web_app)

sql_object.engine.execute('CREATE DATABASE IF NOT EXISTS %s' % DB_NAME)  # create db
sql_object.engine.execute('USE %s' % DB_NAME)  # select db to use

sql_object.create_all(app=web_app)


if __name__ == '__main__':
    web_app.run(
        host=HTTP_HOST,
        port=HTTP_PORT,
        # debug=True
    )