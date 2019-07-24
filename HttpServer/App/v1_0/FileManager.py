from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from flask import send_from_directory
from flask import session
from Exception.SqlException import ObjectNotExist
from Configure.HttpSetting import *
from HttpServer.App.v1_0.AuthManager import AuthManager
from SQLManager.RelationalTableObject.LocationList import LocationList
from SQLManager.RelationalTableObject.GenerateData import GenerateData
from SQLManager.RelationalTableObject.SingleCalibration import SingleCalibration
from SQLManager.RelationalTableObject.StereoCalibration import StereoCalibration
from SQLManager.RelationalTableObject.DH_Optimised import DH_Optimised
from SQLManager.RelationalTableObject.InverseTest import InverseTest
from Configure.DB_Setting import ALLOW_EXTENSIONS


class FileUpload(JsonTranslator):
    table_name_list = [
        GenerateData.__name__,
        SingleCalibration.__name__,
        StereoCalibration.__name__,
        DH_Optimised.__name__,
        InverseTest.__name__
    ]


    def __init__(self):
        self.user_id = session.get(USER_ID_N)
        self.req_data = reqparse.request.data
        self.req_dict = self.to_dict(self.req_data)
        super(FileUpload, self).__init__()

    # @AuthManager.user_auth
    def post(self, location_id, table_name):
        self.logger.info("%s : post" % __name__)
        if table_name not in self.table_name_list:
            return self.make_http_response(False, 'table name must be one of %s' % str(self.table_name_list))
        if self.req_dict is not None and 'is_cover' in self.req_dict and self.req_dict['is_cover'] is True:
            is_cover = True
        else:
            is_cover = False
        loc_obj = LocationList.get_by_id(location_id)
        if loc_obj is None:
            return self.make_http_response(False, 'Location obj is not exist which id is %s' % str(location_id))
        ret_obj = self._save_files(reqparse.request.files.to_dict(), loc_obj, table_name, is_cover)
        return self.make_http_response(True, 'upload result', msg_obj=ret_obj)

    def _save_files(self, files_dict, loc_obj, table_name, is_overwrite):
        if not isinstance(files_dict, dict):
            raise ObjectNotExist("File dict arg is not a type of dict")
        ret_dict = {}
        for k, v in files_dict.items():
            ret_dict[k] = True
            if not is_overwrite and loc_obj.is_own_file(v.filename):
                return self.make_http_response(False, 'file %s has been upload, maybe you want to cover it')
            if not v or not self._filename_check(v.filename):
                ret_dict[k] = False
                continue
            file_path = UPLOAD_FOLDER + str(loc_obj.id) + '/' + table_name
            self._mkdirs(file_path)
            abs_path = file_path + '/' + v.filename
            v.save(abs_path)
        return self.make_http_response(True, 'upload result', msg_obj=ret_dict)

    def _mkdirs(self, path):
        self.logger.info('make dir: %s' % path)
        if os.path.exists(path):
            self.logger.warn('%s is exist, no need to create again')
            return True
        else:
            os.makedirs(path)
            return True

    def _filename_check(self, filename):
        if not isinstance(filename, str):
            return False
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOW_EXTENSIONS


class FileDownload(JsonTranslator):

    def __init__(self):
        super(FileDownload, self).__init__()

    # @AuthManager.user_auth
    def get(self, location_id, table_name, filename):
        self.logger.info('%s: get %s' % (__name__, filename))
        loc_obj = LocationList.get_by_id(location_id)
        if loc_obj is None:
            self.make_http_response(False, 'file not exist')

        file_path = loc_obj.get_upload_path() + '/' + str(table_name) + '/'
        if not os.path.exists(file_path + filename):
            # raise ObjectNotExist('file not exist')
            return self.make_http_response(False, 'file not exist')
        response = send_from_directory(file_path, filename, as_attachment=True)
        response.headers['Content-Disposition'] += "; %s*=utf-8''{}" % filename
        return response




