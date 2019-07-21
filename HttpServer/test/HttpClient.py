# -*- coding:utf-8 -*-

import requests
import time
from socketIO_client import SocketIO, BaseNamespace, LoggingNamespace
import os



IP = '127.0.0.1'
PORT = 8889


class WSGIClient(object):

    url_dict = {
        'login_url': 'http://%s:%d/v1_0/login/' % (IP, PORT),
        'register_url': 'http://%s:%d/v1_0/registrar/' % (IP, PORT),
        'controller_url': 'http://%s:%d/v1_0/WebRobotController/' % (IP, PORT),
        'point_url': 'http://%s:%d/v1_0/point/' % (IP, PORT),
        'upload_url': 'http://%s:%d/v1_0/upload/' % (IP, PORT),
        'download_url': 'http://%s:%d/v1_0/download/' % (IP, PORT),
        'delete_url': 'http://%s:%d/v1_0/delete/' % (IP, PORT),
        'run_file_url': 'http://%s:%d/v1_0/runFile/' % (IP, PORT),
        'control_gain_url': 'http://%s:%d/v1_0/gainController/' % (IP, PORT),
        'logout_url': 'http://%s:%d/v1_0/logout/' % (IP, PORT),
        # 'status_url': 'http://%s:%d/robotstatus/on' % (IP, PORT),
        # 'status_ur_l': 'http://%s:%d/robotstatus/off' % (IP, PORT)
        'camera_url': 'http://%s:%d/v1_0/camera/' % (IP, PORT),
        'stereo_url': 'http://%s:%d/v1_0/stereo/' % (IP, PORT),
    }

    headers_dict = {
        'Content-Type': 'application/json'
    }

    BIG_FILE_MIN_SIZE_BYTE = 1024
    CHUNK_SIZE_BYTE = 1024

    def __init__(self):
        self.request = requests
        self.REQ_STATUS_NAME = 'req_status'
        self.token = None
        self.ws = None
        self.counter = 1
        self.session = self.request.session()

    def login(self, account, password):
        data = {
            'is_login' : True,
            'account'   : '%s' % account,
            'password'  : '%s' % password,
        }
        # sn = self.request.session()
        # if id != -1:
        #     sn.
        ret = self.session.post(
            self.url_dict['login_url'],
            headers=self.headers_dict,
            json=data
        )
        print('>>>', ret.json(), ret.cookies, type(ret))
        # print('<<<:', )
        # self.token = self._get_token(ret.json())
        # return

    def logout(self):
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }
        ret = self.request.post(
            self.url_dict['logout_url'],
            headers=header,
        )
        self.token = self._get_token(ret.json())

    def register(self, account, password):
        obj_data = {
            'account': '%s'.encode() % account,
            'password': '%s'.encode() % password,
            'nickname': '%s'.encode() % "asd"
        }
        data = {
            'obj_data': obj_data
        }
        ret = self.request.post(
            self.url_dict['register_url'],
            headers=self.headers_dict,
            json=data
        )
        print(ret.json())

    def stereo_set(self, l_id, r_id, l_cam_file=None, r_cam_file=None):
        obj_data = {
            'l_camera_id': l_id,
            'r_camera_id': r_id,
            'l_cam_matrix': l_cam_file,
            'r_cam_matrix': r_cam_file
        }
        data = {
            'obj_data': obj_data
        }
        ret = self.session.post(
            self.url_dict['stereo_url'],
            headers=self.headers_dict,
            json=data
        )
        print(ret.json())

    def stereo_get(self):
        data = {
            # 'id': 'abc'
        }
        ret = self.request.get(
            self.url_dict['stereo_url'],
            headers=self.headers_dict,
            json=data
        )
        print(ret.json())

    def camera_post(self):
        obj_data = {
            'id': 'abc',
            'use_type': 'L',
            'producer': 'RR'
        }

        data = {
            'obj_data': obj_data
        }

        ret = self.request.post(
            self.url_dict['camera_url'],
            headers=self.headers_dict,
            json=data
        )
        print(ret.json())

    def camera_post1(self):
        obj_data = {
            'id': 'def',
            'use_type': 'R',
            'producer': 'KENT'
        }

        data = {
            'obj_data': obj_data
        }

        ret = self.request.post(
            self.url_dict['camera_url'],
            headers=self.headers_dict,
            json=data
        )
        print(ret.json())

    def camera_get(self, id=None):
        data = {
            # 'id': 'abc'
        }
        if id is not None:
            ret = self.session.get(
                self.url_dict['camera_url'] + str(id),
                headers=self.headers_dict,
                json=data
            )
        else:
            ret = self.session.get(
                self.url_dict['camera_url'],
                headers=self.headers_dict,
                json=data
            )
        print(ret.json())

    def check_control(self):
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }

        ret = self.request.get(
            self.url_dict['controller_url'],
            headers=header,
        )
        req_respnse = ret.json()
        if self.REQ_STATUS_NAME in req_respnse:
            print('req_status:', req_respnse[self.REQ_STATUS_NAME])
            return req_respnse[self.REQ_STATUS_NAME]
        print('without req_status')
        return False

    def control(self, command):
        data = {
            'cmd': '%s' % command
        }
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }

        ret = self.request.post(
            self.url_dict['controller_url'],
            headers=header,
            json=data
        )
        print('ret:', ret.json())

    def start_get_status(self):
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token

        }
        self.ws = SocketIO(IP, PORT, headers=header)
        # self.ws.connect()
        self.ws.on('robot_status', self.on_message_client)
        time.sleep(1)
        self.ws.emit('join', "on")
        self.counter = 0

    def stop_get_status(self):
        print(">>>stop_get_status")
        self.ws.emit('leave', "on")

    def _get_token(self, data):
        print('>>> %s' % data)
        if isinstance(data, str):
            print('Args invalid')
            return None
        if 'data' in data and 'token' in data['data']:
            print("===%s" % data['data']['token'])
            return data['data']['token']
        else:
            print('get token failed')
        return None

    def get_point(self, id):
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }
        # print('>>>>>>%s' % (self.url_dict['point_url'] + '%d' % id))
        ret = self.request.get(
            self.url_dict['point_url'] + '%d' % id,
            headers=header
        )
        print('get_point:%s' % ret.json())

    def delete_point(self, id):
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }

        ret = self.request.delete(
            self.url_dict['point_url'] + '%d' % id,
            headers=header
        )
        print('delete_point:%s' % ret.json())

    def add_point(self, id):
        data = {
            'Id': '%d' % id,
            'Data': '(0,0,0,0,1,0)',
            'Description': 'test',
            'Elbow': 'T',
            'Hand': 'R'
        }
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }

        ret = self.request.put(
            self.url_dict['point_url'] + '%d' % id,
            headers=header,
            json=data
        )
        print('add_point:%s' % ret.json())

    def edit_point(self, id):
        data = {
            'Id': '%d' % id,
            'Data': '(360,0,0,0,1,0)',
            'Description': 'test',
            'Elbow': 'T',
            'Hand': 'R'
        }
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }

        ret = self.request.post(
            self.url_dict['point_url'] + '%d' % id,
            headers=header,
            json=data
        )
        print('edit_point:%s' % ret.json())


    def on_message_client(self, *args):
        print(">>>>>>%d: %s" % (self.counter, args))
        # print("!!!", self.counter)
        self.counter += 1

    # def check_files(self, *args):
    #     for item in args:
    #         if not os.path.exists(item):
    #             return False
    #     return True

    # def get_filename(self, path):
    #     if not isinstance(path, str):
    #         return None

    def files_upload(self, file_list):
        print('files_upload: %s' % str(file_list))
        files_dict = {}
        for item in file_list:
            print('item: %s' % str(item))
            if not os.path.isfile(item):
                return False
            files_dict[os.path.basename(item)] = open(item, 'rb')
        # file_open = open('./upload_test/lua1.lua', 'rb')
        # files_dict = {
        #     'lua1.lua': file_open
        # }
        print('---', files_dict)
        # print '---', files_dict['lua1.lua'].read()

        header = {
            # 'Content-Type': 'multipart/form-data',
            # 'Authorization': 'jwt %s' % self.token
        }
        ret = self.request.post(
            self.url_dict['upload_url'],
            headers=header,
            files=files_dict
        )
        print('files_upload: %s' % ret.json())

    def file_download(self, filename, file_dir):
        print('files_download: %s' % str(filename))
        if not os.path.exists(file_dir):
            print('Download directory is not exist')
            return None
        header = {
            # 'Content-Type': 'multipart/form-data',
            'Authorization': 'jwt %s' % self.token
        }
        # filename_list = self.get_download_list()
        # if filename not in filename_list:
        #     print('Failed to download, without this filename')
        #     return None
        download_file_stream = self.session.get(
            self.url_dict['download_url'] + filename,
            headers=header,
            stream=True
        )
        # print('ret:', download_file_stream.json())
        self.save_file_from_http_response(download_file_stream, file_dir, filename)

    def file_download_all(self, file_dir):
        print('file_download_all: %s' % str(file_dir))
        if not os.path.exists(file_dir):
            print('Download directory is not exist')
            return None
        header = {
            # 'Content-Type': 'multipart/form-data',
            'Authorization': 'jwt %s' % self.token
        }
        filename_list = self.get_download_list()
        for filename in filename_list:
            download_file_stream = self.request.get(
                self.url_dict['download_url'] + filename,
                headers=header,
                stream=True
            )
            self.save_file_from_http_response(download_file_stream, file_dir, filename)

    def save_file_from_http_response(self, download_file_stream, file_dir, filename):
        # print('download_req:', download_file_stream.content)
        # print('download_req type:', type(download_file_stream.content))
        # if isinstance(download_file_stream, )
        # print('res type: ', type(download_file_stream))
        # print('res type111: ', type(download_file_stream.content))
        # print('res type111: ', download_file_stream.headers)
        if download_file_stream.headers['Content-Type'] == 'application/json':
            print('ret: ', download_file_stream.json())
            return None
        if not file_dir.endswith('/'):
            file_absolute_path = file_dir + '/' + filename
        else:
            file_absolute_path = file_dir + filename
        download_file = open(file_absolute_path, 'wb')

        if download_file_stream.headers['Content-Length'] <= self.BIG_FILE_MIN_SIZE_BYTE:
            download_file.write(download_file_stream.content)
        else:
            for chunk in download_file_stream.iter_content(chunk_size=self.CHUNK_SIZE_BYTE):
                if chunk:
                    download_file.write(chunk)
        download_file.close()

    def get_download_list(self):
        print('get_download_list:')
        header = {
            # 'Content-Type': 'multipart/form-data',
            'Authorization': 'jwt %s' % self.token
        }
        ret = self.request.get(
            self.url_dict['download_url'] + 'getList',
            headers=header
        )

        ret_json = ret.json()
        print('files_download: %s' % ret_json)
        if 'data' not in ret_json:
            print('Failed to download')
            return None

        file_dict = ret.json()['data']
        print('file_dict: %s' % file_dict)

        if 'filename list' not in file_dict:
            print('Failed to download')
            return None
        filename_list = file_dict['filename list']
        print('filename_list:', filename_list)
        return filename_list

        # ret = self.request.get(
        #     self.url_dict['download_url'],
        #     headers=header,
        #     files=files_dict
        # )
        # print('files_download: %s' % ret.json())

    def delete_file(self, filename):
        print('delete_file:')
        header = {
            # 'Content-Type': 'multipart/form-data',
            'Authorization': 'jwt %s' % self.token
        }
        ret = self.request.post(
            self.url_dict['delete_url'] + filename,
            headers=header
        )
        print('delete_file: %s' % ret.json())

    def check_run_file(self, filename):
        print('check_run_file:')
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }
        ret = self.request.get(
            self.url_dict['run_file_url'] + filename,
            headers=header,
        )
        req_respnse = ret.json()
        print('req_respnse:', req_respnse)
        if self.REQ_STATUS_NAME in req_respnse:
            print('req_status:', req_respnse[self.REQ_STATUS_NAME])
            return req_respnse[self.REQ_STATUS_NAME]
        print('without req_status')
        return False

    def run_file(self, filename):

        print('run_file:')
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }
        ret = self.request.post(
            self.url_dict['run_file_url'] + filename,
            headers=header
        )
        print('run_file: %s' % ret.json())

    def gain_controller(self):

        print('gain_controller:')
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }
        ret = self.request.post(
            self.url_dict['control_gain_url'] + 'ON',
            headers=header
        )
        print('gain_controller: %s' % ret.json())

    def left_controller(self):
        print('run_file:')
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }
        ret = self.request.post(
            self.url_dict['control_gain_url'] + 'OFF',
            headers=header
        )
        print('left_controller: %s' % ret.json())

def goja_test():
    client = WSGIClient()
    client.login(test_account, test_password, test_robot_type, test_robot_joints)
    is_enable_control = client.check_control()
    if not is_enable_control:
        print('without priority to control the robot')
        return False
    client.gain_controller()
    client.control('setSpeed(80)')
    client.control('setAccel(80)')
    while True:
        client.control('goja(-90,-90,0,0,0,0)')
        time.sleep(2)
        client.control('goja(-90,-90,-200,0,0,0)')
        time.sleep(1)
        client.control('goja(-90,-90,-200,200,0,0)')
        time.sleep(1)
        client.control('goja(-90,-90,0,200,0,0)')
        time.sleep(1)
        client.control('goja(90,90,0,200,0,0)')
        time.sleep(2)
        client.control('goja(90,90,-200,200,0,0)')
        time.sleep(1)
        client.control('goja(90,90,-200,0,0,0)')
        time.sleep(1)
        client.control('goja(90,90,0,0,0,0)')
        time.sleep(1)
    print('finishing control the robot')
    return True

def get_status_test():
    root_client = WSGIClient()
    root_client.login(root_account, root_password, root_robot_type, root_robot_joints)
    # admin_client.login(admin_account, admin_password, admin_robot_type, admin_robot_joints)
    # admin_client.start_get_status()
    root_client.start_get_status()
    while True:
        print('waiting...')
        root_client.ws.wait()
        # time.sleep(1)

def login_test():
    admin_client = WSGIClient()
    root_client = WSGIClient()
    root_client.login(root_account, root_password, root_robot_type, root_robot_joints)
    admin_client.login(admin_account, admin_password, admin_robot_type, admin_robot_joints)
    admin_client.control('setSpeed(80)')
    admin_client.control('Y')
    admin_client.control('setSpeed(80)')
    admin_client.control('setAccel(80)')
    root_client.control('setSpeed(80)')
    root_client.control('Y')
    root_client.control('setSpeed(80)')
    root_client.control('setAccel(80)')
    time.sleep(15)
    admin_client.login(admin_account, admin_password, admin_robot_type, admin_robot_joints)
    admin_client.control('setSpeed(80)')
    admin_client.control('Y')
    admin_client.control('setSpeed(80)')
    admin_client.control('setAccel(80)')

def points_test():
    point_id = 5
    client = WSGIClient()
    client.login(admin_account, admin_password, admin_robot_type, admin_robot_joints)
    client.get_point(point_id)
    client.add_point(point_id)
    client.add_point(point_id + 1)
    client.get_point(point_id)
    client.edit_point(point_id)
    client.get_point(point_id)
    client.delete_point(point_id)
    client.get_point(point_id)


def upload_test():

    file_list = (
        './upload_test/lua1.lua',
        './upload_test/lua2.txt',
        './upload_test/lua3.lua',
        './upload_test/lua4.lua',
        './upload_test/lua5.lua',
        './upload_test/test.pts',
        './upload_test/temp.txt',
    )
    client = WSGIClient()
    # client.login(admin_account, admin_password, admin_robot_type, admin_robot_joints)
    client.login(test_account, test_password, test_robot_type, test_robot_joints)
    # client.login(root_account, root_password, root_robot_type, root_robot_joints)
    client.files_upload(file_list)

def download_test():
    client = WSGIClient()
    client.login(test_account, test_password, test_robot_type, test_robot_joints)
    # client.login(root_account, root_password, root_robot_type, root_robot_joints)
    # client.login(admin_account, admin_password, admin_robot_type, admin_robot_joints)
    client.file_download('lua99.lua', './download_test/')
    client.file_download_all('./download_test/')

def delete_test():
    client = WSGIClient()
    client.login(test_account, test_password, test_robot_type, test_robot_joints)
    # client.login(root_account, root_password, root_robot_type, root_robot_joints)
    # client.login(admin_account, admin_password, admin_robot_type, admin_robot_joints)
    client.delete_file('temp.txt')
    client.delete_file('lua4.lua')

def run_file_test():
    client = WSGIClient()
    client.login(test_account, test_password, test_robot_type, test_robot_joints)
    # client.run_file('qqqq')
    # time.sleep(18)
    client.gain_controller()
    ret_status = client.check_run_file('lua1.lua')
    client.logout()
    if ret_status:
        client.run_file('Y')
        client.run_file('Y')
        client.run_file('qqqq')
        client.run_file('lua1.lua')
        return True
    else:
        print('cannot run lua1.lua file')
        return False

test_account = 'test'
test_password = '123456'
test_robot_type = 'KENT'
test_robot_joints = 4

root_account = 'Ban'
root_password = '123456'
root_robot_type = 'KENT'
root_robot_joints = 6

admin_account = 'peng_ban'
admin_password = '123456'
admin_robot_type = 'KENT'
admin_robot_joints = 4

if __name__ == '__main__':
    web_client = WSGIClient()
    # 注册
    # web_client.register('ban', '123123')

    # 登录
    # web_client.login('ban', 123123)

    # 添加相机， 重复添加报错， 每次返回数据包包含 请求结果信息
    # web_client.camera_post()
    # web_client.camera_post1()

    # 获取相机列表
    web_client.camera_get()
    web_client.camera_get('abc')

    # 上传文件， 用户绑定
    # web_client.files_upload(['/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/lua2.txt',
    #                          '/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/c.txt',
    #                          '/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/a.png',
    #                          '/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/d.txt',
    #                          '/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/e.txt'
    #                          ])

    # 添加双目标定结果表信息
    # web_client.stereo_set('abc', 'def', 'lua2.txt', 'e.txt')
    #
    # # 获取双目标定结果表信息
    # web_client.stereo_get()

    # 下载文件
    # web_client.file_download('c.txt', './download_test/')



