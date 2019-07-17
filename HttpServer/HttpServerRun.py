from flask_restful import Api
from flask import Flask
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.Configure import DB_Setting
from SQLManager.Configure.DB_Setting import DB_NAME
from HttpServer.Configure.HttpSetting import *


def url_init(api_obj):
    from HttpServer.App.v1_0.UserManager import Registrar, Login
    from HttpServer.App.v1_0.CameraManager import CameraManager
    from HttpServer.App.v1_0.FileManager import FileUpload, FileDownload
    from HttpServer.App.v1_0.StereoManager import StereoManager

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

    api_obj.add_resource(
        CameraManager,
        '/v1_0/camera/',
        endpoint='Camera'
    )

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

    api_obj.add_resource(
        StereoManager,
        '/v1_0/stereo/',
        endpoint='Stereo'
    )



def create_app(configure_file):
    new_app = Flask(__name__)

    web_api = Api(new_app)

    url_init(web_api)

    new_app.config.from_object(configure_file)

    return new_app


web_app = create_app(DB_Setting)
web_app.app_context().push()


@web_app.teardown_request
def teardown_request(exception):
    BaseObject.commit()
    if exception is not None:
        print(exception)


sql_object.init_app(web_app)

sql_object.engine.execute('CREATE DATABASE IF NOT EXISTS %s' % DB_NAME)  # create db
sql_object.engine.execute('USE %s' % DB_NAME)  # select db to use

sql_object.create_all(app=web_app)


if __name__ == '__main__':
    web_app.run(
        host=HTTP_HOST,
        port=HTTP_PORT,
        debug=False
    )