from HttpServer.Translator.JsonTranslator import JsonTranslator
from flask_restful import reqparse
from SQLManager.RelationalTableObject.StereoCalibration import StereoCalibration
from SQLManager.Exception.SqlException import *
from HttpServer.Configure.HttpSetting import *
from SQLManager.Configure.DB_Setting import *
from SQLManager.RelationalTableObject.User import User


class FileUpload(JsonTranslator):

    def __init__(self):
        super(FileUpload, self).__init__()

    def get(self):
        print("%s : get" % self.__name__)
        # default
        test_user = User.get_by_account('ban')
        ret_obj = self._save_files(reqparse.request.files.to_dict(), test_user)
        return self.make_http_response('upload result', msg_obj=ret_obj)

    def _save_files(self, files_dict, user):
        if not isinstance(files_dict, dict):
            raise ObjectNotExist("File dict is not a dict")
        ret_dict = {}
        for k, v in files_dict.items():
            ret_dict[k] = True

            if not v or not self._filename_check(v.filename):
                ret_dict[k] = False
                continue
            file_path = UPLOAD_ROOT_URI + user.id
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