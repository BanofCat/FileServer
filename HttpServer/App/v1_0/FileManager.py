from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from HttpServer.Configure.HttpSetting import *
from SQLManager.Configure.DB_Setting import *
from SQLManager.RelationalTableObject.User import User
from flask import send_from_directory
from flask import session

class FileUpload(JsonTranslator):

    def __init__(self):
        self.user_id = session.get(USER_ID_N)
        super(FileUpload, self).__init__()

    def post(self):
        print("%s : post" % __name__)
        ret_obj = self._save_files(reqparse.request.files.to_dict(), test_user)
        return self.make_http_response(True, 'upload result', msg_obj=ret_obj)

    def _save_files(self, files_dict, user):
        if not isinstance(files_dict, dict):
            raise ObjectNotExist("File dict arg is not a type of dict")
        ret_dict = {}
        for k, v in files_dict.items():
            ret_dict[k] = True

            if not v or not self._filename_check(v.filename):
                ret_dict[k] = False
                continue
            file_path = UPLOAD_FOLDER + str(user.id)
            self._mkdirs(file_path)
            abs_path = file_path + '/' + v.filename
            v.save(abs_path)
        return ret_dict

    def _mkdirs(self, path):
        print('make dir: %s' % path)
        if os.path.exists(path):
            print('%s is exist, no need to create again')
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

    def get(self, filename):
        # default
        print('filename: ', filename)
        test_user = User.get_by_account('ban')
        file_path = test_user.get_upload_path()
        if not os.path.exists(file_path + filename):
            raise ObjectNotExist('file not exist')
        response = send_from_directory(file_path, filename, as_attachment=True)
        response.headers['Content-Disposition'] += "; %s*=utf-8''{}" % filename
        return response




