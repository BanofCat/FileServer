# -*- coding:utf-8 -*-

import requests
import os
import datetime


IP = '127.0.0.1'
PORT = 8889
API_VERSION = 'v1_0'


class WSGIClient(object):

    root_url = 'http://%s:%d/%s' %(IP, PORT, API_VERSION)

    url_dict = {
        'login_url':        root_url + '/login/',
        'register_url':     root_url + '/registrar/',
        'upload_url':       root_url + '/upload/',
        'download_url':     root_url + '/download/',
        'logout_url':       root_url + '/logout/',
        'camera_url':       root_url + '/camera/',
        'stereo_url':       root_url + '/stereo/',
        'location_url':     root_url + '/location/',
        'generate_url':     root_url + '/generate/',
        'robot_url':        root_url + '/robot/',
        'dh_url':        root_url + '/dh/',
        'inverse_url':        root_url + '/inverse/',
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
        ret = self.session.post(
            self.url_dict['login_url'],
            headers=self.headers_dict,
            json=data
        )
        print('>>>', ret.json(), ret.cookies, type(ret))

    def logout(self):
        header = {
            'Content-Type': 'application/json',
            'Authorization': 'jwt %s' % self.token
        }
        ret = self.session.post(
            self.url_dict['logout_url'],
            headers=header,
        )

    def register(self, account, password):
        obj_data = {
            'account': '%s'.encode() % account,
            'password': '%s'.encode() % password,
            'nickname': '%s'.encode() % "asd"
        }
        data = {
            'obj_data': obj_data
        }
        ret = self.session.post(
            self.url_dict['register_url'],
            headers=self.headers_dict,
            json=data
        )
        print ret.json()

    def _obj_add(self, obj_data, url, is_add, loc_id=None):
        data = {
            'obj_data': obj_data
        }
        if loc_id is None:
            loc_id = ''
        if is_add:
            ret = self.session.post(
                url,
                headers=self.headers_dict,
                json=data
            )
        else:
            ret = self.session.put(
                url + str(loc_id),
                headers=self.headers_dict,
                json=data
            )
        print('ret:', ret, type(ret))
        print(ret.json())

    def _obj_delete(self, url, id):
        data = {}
        ret = self.session.delete(
            url + str(id),
            headers=self.headers_dict,
            json=data
        )
        print ret.json()

    def _obj_get(self, url, data=None, id=None):
        if data is None:
            data = {}
        if id is None:
            id = ''
        ret = self.session.get(
            url + str(id),
            headers=self.headers_dict,
            json=data
        )
        print ret.json()

    # robot api
    def _robot_pack(self, id, joints, type):
        obj_data = {
            'id': id,
            'joints': joints,
            'type': type,
        }
        return obj_data

    def robot_add(self, id, joints, type):
        obj_data =  self._robot_pack(id, joints, type)
        return self._obj_add(obj_data, self.url_dict['robot_url'], True)

    def robot_update(self, id, joints=None, type=None):
        obj_data =  self._robot_pack(id, joints, type)
        return self._obj_add(obj_data, self.url_dict['robot_url'], False)

    def robot_delete(self, id):
        return self._obj_delete(self.url_dict['robot_url'], id)

    def robot_get(self, id=None):
        return self._obj_get(self.url_dict['robot_url'], id=id)

    # camera api
    def _camera_pack(self, id, use_type, producer):
        obj_data = {
            'id': id,
            'use_type': use_type,
            'producer': producer
        }
        return obj_data

    def camera_add(self, id, use_type, producer):
        obj_data = self._camera_pack(id, use_type, producer, )
        return self._obj_add(obj_data, self.url_dict['camera_url'], True)

    def camera_update(self, id, use_type=None, producer=None):
        obj_data = self._camera_pack(id, use_type, producer)
        return self._obj_add(obj_data, self.url_dict['camera_url'], False)

    def camera_get(self, id=None):
        return self._obj_get(self.url_dict['camera_url'], id=id)

    def camera_delete(self, id):
        return self._obj_delete(self.url_dict['camera_url'], id)

    # generate data API
    def _generate_pack(self, r_id, u_id, g_id=None, pic_date=None, dh_date=None, fb_date=None):
        obj_data = {
            'id': g_id,
            'robot_id': r_id,
            'user_id': u_id,
            'pic_date': pic_date,
            'dh_date': dh_date,
            'fb_date': fb_date
        }
        return obj_data

    def generate_add(self, r_id, u_id, pic_date=None, dh_date=None, fb_date=None):
        obj_data = self._generate_pack(r_id, u_id, pic_date, dh_date, fb_date)
        return self._obj_add(obj_data, self.url_dict['generate_url'], True)

    def generate_update(self, g_id, r_id=None, u_id=None, pic_date=None, dh_date=None, fb_date=None):
        obj_data = self._generate_pack(r_id, u_id, g_id, pic_date, dh_date, fb_date)
        return self._obj_add(obj_data, self.url_dict['generate_url'], False)

    def generate_delete(self, id):
        return self._obj_delete(self.url_dict['generate_url'], id)

    def generate_get(self, id=None):
        return self._obj_get(self.url_dict['generate_url'], id=id)

    # stereo API
    def _stereo_pack(self, l_id, r_id, l_cam_matrix=None, r_cam_matrix=None, l_dist_coeffs=None, r_dist_coeffs=None,
                     rt_cam_a2_cam_b=None, stereo_e=None, stereo_f=None, stereo_r=None, pixel_err=None):
        obj_data = {
            'l_camera_id': l_id,
            'r_camera_id': r_id,
            'l_cam_matrix': l_cam_matrix,
            'r_cam_matrix': r_cam_matrix,
            'l_dist_coeffs': l_dist_coeffs,
            'r_dist_coeffs': r_dist_coeffs,
            'rt_cam_a2_cam_b': rt_cam_a2_cam_b,
            'stereo_E': stereo_e,
            'stereo_F': stereo_f,
            'stereo_R': stereo_r,
            'pixel_err': pixel_err,

        }
        return obj_data

    def stereo_add(self, l_id, r_id, l_cam_matrix=None, r_cam_matrix=None, l_dist_coeffs=None, r_dist_coeffs=None,
                     rt_cam_a2_cam_b=None, stereo_e=None, stereo_f=None, stereo_r=None, pixel_err=None):
        obj_data =  self._stereo_pack(l_id, r_id, l_cam_matrix, r_cam_matrix, l_dist_coeffs, r_dist_coeffs,
                     rt_cam_a2_cam_b, stereo_e, stereo_f, stereo_r, pixel_err)
        return self._obj_add(obj_data, self.url_dict['stereo_url'], True)

    def stereo_update(self, loc_id, l_id, r_id, l_cam_matrix=None, r_cam_matrix=None, l_dist_coeffs=None, r_dist_coeffs=None,
                     rt_cam_a2_cam_b=None, stereo_e=None, stereo_f=None, stereo_r=None, pixel_err=None):
        obj_data =  self._stereo_pack(l_id, r_id, l_cam_matrix, r_cam_matrix, l_dist_coeffs, r_dist_coeffs,
                     rt_cam_a2_cam_b, stereo_e, stereo_f, stereo_r, pixel_err)
        return self._obj_add(obj_data, self.url_dict['stereo_url'], False, loc_id)

    def stereo_get(self, id=None):
        return self._obj_get(self.url_dict['stereo_url'], id=id)

    # single API
    def _single_pack(self, camera_id, n_camera_args=None, p_camera_args=None, n_distortion=None, p_distortion=None,
                     n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None, found_mask=None,
                     img_pts=None, img_size=None, obj_ptr=None):
        obj_data = {
            'camera_id': camera_id,
            'n_camera_args': n_camera_args,
            'p_camera_args': p_camera_args,
            'n_distortion': n_distortion,
            'p_distortion': p_distortion,
            'n_toc': n_toc,
            'p_toc': p_toc,
            'n_projection_err': n_projection_err,
            'p_projection_err': p_projection_err,
            'found_mask': found_mask,
            'img_pts': img_pts,
            'img_size': img_size,
            'obj_ptr': obj_ptr
        }
        return obj_data

    def single_add(self, camera_id, n_camera_args=None, p_camera_args=None, n_distortion=None, p_distortion=None,
                     n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None, found_mask=None,
                     img_pts=None, img_size=None, obj_ptr=None):
        obj_data =  self._single_pack(camera_id, n_camera_args, p_camera_args, n_distortion, p_distortion,
                     n_toc, p_toc, n_projection_err, p_projection_err, found_mask,
                     img_pts, img_size, obj_ptr)
        return self._obj_add(obj_data, self.url_dict['single_url'], True)

    def single_update(self, loc_id, camera_id, n_camera_args=None, p_camera_args=None, n_distortion=None, p_distortion=None,
                     n_toc=None, p_toc=None, n_projection_err=None, p_projection_err=None, found_mask=None,
                     img_pts=None, img_size=None, obj_ptr=None):
        obj_data =  self._single_pack(camera_id, n_camera_args, p_camera_args, n_distortion, p_distortion,
                     n_toc, p_toc, n_projection_err, p_projection_err, found_mask,
                     img_pts, img_size, obj_ptr)
        return self._obj_add(obj_data, self.url_dict['single_url'], False, loc_id)

    def single_get(self, id=None):
        return self._obj_get(self.url_dict['single_url'], id=id)


    # DH optimise API
    def _dh_pack(self, model, angle_offset_full=None, joint_scale_factor=None, refine_pixel_err=None,
                robot_parm=None, tot=None, trc=None, a_offset_six_parm=None, c_offset_six_parm=None):
        obj_data = {
            'model': model,
            'angle_offset_full': angle_offset_full,
            'joint_scale_factor': joint_scale_factor,
            'refine_pixel_err': refine_pixel_err,
            'robot_parm': robot_parm,
            'tot': tot,
            'trc': trc,
            'a_offset_six_parm': a_offset_six_parm,
            'c_offset_six_parm': c_offset_six_parm
        }
        return obj_data

    def dh_add(self, model, angle_offset_full=None, joint_scale_factor=None, refine_pixel_err=None,
                robot_parm=None, tot=None, trc=None, a_offset_six_parm=None, c_offset_six_parm=None):
        obj_data =  self._dh_pack(model, angle_offset_full, joint_scale_factor, refine_pixel_err,
                robot_parm, tot, trc, a_offset_six_parm, c_offset_six_parm)
        return self._obj_add(obj_data, self.url_dict['dh_url'], True)

    def dh_update(self, loc_id, model, angle_offset_full=None, joint_scale_factor=None, refine_pixel_err=None,
                robot_parm=None, tot=None, trc=None, a_offset_six_parm=None, c_offset_six_parm=None):
        obj_data =  self._dh_pack(model, angle_offset_full, joint_scale_factor, refine_pixel_err,
                robot_parm, tot, trc, a_offset_six_parm, c_offset_six_parm)
        return self._obj_add(obj_data, self.url_dict['dh_url'], False, loc_id)

    def dh_get(self, id=None):
        return self._obj_get(self.url_dict['dh_url'], id=id)


    # inverse optimise API
    def _inverse_pack(self, opt_all_ik=None, ik_err=None, l_cam_img_pts=None, r_cam_img_pts=None,
                pixel_err=None, total_pixel_err=None):
        obj_data = {
            'opt_all_ik': opt_all_ik,
            'ik_err': ik_err,
            'l_cam_img_pts': l_cam_img_pts,
            'r_cam_img_pts': r_cam_img_pts,
            'pixel_err': pixel_err,
            'total_pixel_err': total_pixel_err,
        }
        return obj_data

    def inverse_add(self, opt_all_ik=None, ik_err=None, l_cam_img_pts=None, r_cam_img_pts=None,
                pixel_err=None, total_pixel_err=None):
        obj_data =  self._inverse_pack(opt_all_ik, ik_err, l_cam_img_pts, r_cam_img_pts, pixel_err, total_pixel_err)
        return self._obj_add(obj_data, self.url_dict['inverse_url'], True)

    def inverse_update(self, loc_id, opt_all_ik=None, ik_err=None, l_cam_img_pts=None, r_cam_img_pts=None,
                pixel_err=None, total_pixel_err=None):
        obj_data =  self._inverse_pack(opt_all_ik, ik_err, l_cam_img_pts, r_cam_img_pts, pixel_err, total_pixel_err)
        return self._obj_add(obj_data, self.url_dict['inverse_url'], False, loc_id)

    def inverse_get(self, id=None):
        return self._obj_get(self.url_dict['inverse_url'], id=id)

    # location optimise API
    def _location_pack(self, g_id, sin_c_id=None, ste_c_id=None, dh_id=None, inv_id=None):
        obj_data = {
            'g_id': g_id,
            'single_ca_id': sin_c_id,
            'stereo_ca_id': ste_c_id,
            'dh_id': dh_id,
            'inv_id': inv_id
        }
        return obj_data

    def location_add(self, g_id, sin_c_id=None, ste_c_id=None, dh_id=None, inv_id=None):
        obj_data =  self._location_pack(g_id, sin_c_id, ste_c_id, dh_id, inv_id)
        return self._obj_add(obj_data, self.url_dict['location_url'], True)

    def location_update(self, loc_id, g_id=None, sin_c_id=None, ste_c_id=None, dh_id=None, inv_id=None):
        obj_data = self._location_pack(g_id, sin_c_id, ste_c_id, dh_id, inv_id)
        return self._obj_add(obj_data, self.url_dict['location_url'], False, loc_id)

    def location_get(self, id=None):
        return self._obj_get(self.url_dict['location_url'], id=id)





    def files_upload(self, file_list):
        print 'files_upload: %s' % str(file_list)
        files_dict = {}
        for item in file_list:
            print 'item: %s' % str(item)
            if not os.path.isfile(item):
                return False
            files_dict[os.path.basename(item)] = open(item, 'rb')
        # file_open = open('./upload_test/lua1.lua', 'rb')
        # files_dict = {
        #     'lua1.lua': file_open
        # }
        print '---', files_dict
        # print '---', files_dict['lua1.lua'].read()

        header = {
            # 'Content-Type': 'multipart/form-data',
            # 'Authorization': 'jwt %s' % self.token
        }
        ret = self.session.post(
            self.url_dict['upload_url'],
            headers=header,
            files=files_dict
        )
        print('files_upload: %s' % ret.json())

    def file_download(self, filename, file_dir):
        print 'files_download: %s' % str(filename)
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
        print 'file_download_all: %s' % str(file_dir)
        if not os.path.exists(file_dir):
            print('Download directory is not exist')
            return None
        header = {
            # 'Content-Type': 'multipart/form-data',
            'Authorization': 'jwt %s' % self.token
        }
        filename_list = self.get_download_list()
        for filename in filename_list:
            download_file_stream = self.session.get(
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
        ret = self.session.get(
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

        # ret = self.session.get(
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
        ret = self.session.post(
            self.url_dict['delete_url'] + filename,
            headers=header
        )
        print('delete_file: %s' % ret.json())



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

def robot_test():
    client = WSGIClient()
    client.robot_get()
    client.robot_add('IronMan', '5', 'RR')
    client.robot_add('BatMan', '4', 'KENT')
    client.robot_get()
    client.robot_get('IronMan')
    client.robot_update('IronMan', '4')
    client.robot_get('IronMan')
    client.robot_delete('IronMan')
    client.robot_get('IronMan')
    client.robot_get()

def camera_test():
    client = WSGIClient()
    client.camera_get()
    client.camera_add('Google', 'L', 'RR')
    client.camera_add('MicroSoft', 'R', 'KENT')
    client.camera_get()
    client.camera_get('Google')
    client.camera_update('Google', 'M')
    client.camera_get('Google')
    client.camera_delete('Google')
    client.camera_get('Google')
    client.camera_get()


def generate_test():
    client = WSGIClient()
    client.generate_get()
    client.generate_add('IronMan', 1, str(datetime.datetime.now()), str(datetime.datetime.now()))
    client.generate_add('BatMan', 1, str(datetime.datetime.now()), str(datetime.datetime.now()))
    client.generate_add('kr4-02', 1, str(datetime.datetime.now()), str(datetime.datetime.now()))
    client.generate_get()
    client.generate_get(2)
    client.generate_update(g_id=2, r_id='BatMan', u_id=1, pic_date=str(datetime.datetime.now()))
    client.generate_get(2)
    client.generate_delete(3)
    client.generate_get(2)
    client.generate_get()


def location_test():
    client = WSGIClient()
    # client.location_get()
    # client.location_add(g_id=1)
    # client.location_add(g_id=2)
    # client.location_add(g_id=3)
    # client.location_get()
    # client.location_get(1)
    client.location_update(loc_id=1, g_id=2)
    # client.location_get(2)
    # client.location_get()


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
    location_test()
    # generate_test()
    # robot_test()
    # camera_test()
    # web_client = WSGIClient()
    # 注册
    # web_client.register('ban', '123123')

    # 登录
    # web_client.login('ban', 123123)

    # 添加相机， 重复添加报错， 每次返回数据包包含 请求结果信息
    # web_client.camera_post()
    # web_client.camera_post1()
    # web_client.camera_put()

    # 获取相机列表
    # web_client.camera_get()
    # web_client.camera_get('abc')

    # 上传文件， 用户绑定
    # web_client.files_upload(['/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/lua2.txt',
    #                          '/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/c.txt',
    #                          '/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/a.png',
    #                          '/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/d.txt',
    #                          '/home/ban/Ban/Ban/work/version4/Develop/develop/Flask_WebServer/WebRC/upload_file/1/e.txt'
    #                          ])

    # 添加机械手
    # web_client.robot_set('kr4-01', '4', 'RR')
    # web_client.robot_set('kr4-02', '4', 'KENT')
    # web_client.robot_get('kr4_01')

    # web_client.robot_delete('kr4-01')
    # web_client.robot_get()

    # 创建总概表
    # web_client.generate_set('kr4-01', '1')

    # 创建Location关系表
    # web_client.location_set()

    # 添加双目标定结果表信息
    # web_client.stereo_set('abc', 'def', 'lua2.txt', 'e.txt')
    # web_client.stereo_update('def', 'abc', 'e.txt', 'c.txt')
    #
    # # 获取双目标定结果表信息
    # web_client.stereo_get()

    # 下载文件
    # web_client.file_download('c.txt', './download_test/')



