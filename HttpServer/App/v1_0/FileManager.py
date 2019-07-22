from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from flask import send_from_directory
from flask import session
from Exception.SqlException import ObjectNotExist
from Configure.HttpSetting import *
from HttpServer.App.v1_0.AuthManager import AuthManager
from SQLManager.RelationalTableObject.LocationList import LocationList


class FileUpload(JsonTranslator):

    def __init__(self):
        self.user_id = session.get(USER_ID_N)
        self.req_dict = self.to_dict(self.req_data)
        super(FileUpload, self).__init__()

    # @AuthManager.user_auth
    def post(self, location_id):
        self.logger.info("%s : post" % __name__)
        if 'is_cover' in self.req_dict and self.req_dict['is_cover'] is True:
            is_cover = True
        else:
            is_cover = False
        loc_obj = LocationList.get_by_id(location_id)
        if loc_obj is None:
            return self.make_http_response(False, 'Location id is wrong')
        ret_obj = self._save_files(reqparse.request.files.to_dict(), loc_obj, is_cover)
        return self.make_http_response(True, 'upload result', msg_obj=ret_obj)

    def _save_files(self, files_dict, loc_obj, is_overwrite):
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
            file_path = UPLOAD_FOLDER + str(loc_obj.id)
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

    @AuthManager.user_auth
    def get(self, req_uer, filename):
        self.logger.info('%s: get %s' % (__name__, filename))
        file_path = req_uer.get_upload_path()
        if not os.path.exists(file_path + filename):
            # raise ObjectNotExist('file not exist')
            return self.make_http_response(False, 'file not exist')
        response = send_from_directory(file_path, filename, as_attachment=True)
        response.headers['Content-Disposition'] += "; %s*=utf-8''{}" % filename
        return response




