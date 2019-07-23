# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from SQLManager.RelationalTableObject.GenerateData import GenerateData
from SQLManager.RelationalTableObject.DH_Optimised import DH_Optimised
from SQLManager.RelationalTableObject.InverseTest import InverseTest
from SQLManager.RelationalTableObject.SingleCalibration import SingleCalibration
from SQLManager.RelationalTableObject.StereoCalibration import StereoCalibration
from Configure.HttpSetting import *
from Exception.SqlException import ObjectNotExist


class LocationList(sql_object.Model, BaseObject):

    __tablename__ = 'LocationList'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    g_id = sql_object.Column(sql_object.Integer, sql_object.ForeignKey('GenerateData.id'), nullable=False)

    single_ca_id = sql_object.Column(sql_object.Integer, sql_object.ForeignKey('SingleCalibration.id'), nullable=True)

    stereo_ca_id = sql_object.Column(sql_object.Integer, sql_object.ForeignKey('StereoCalibration.id'), nullable=True)

    dh_id = sql_object.Column(sql_object.Integer, sql_object.ForeignKey('DH_Optimised.id'), nullable=True)

    inv_id = sql_object.Column(sql_object.Integer, sql_object.ForeignKey('InverseTest.id'), nullable=True)

    def __init__(self, g_id=None, single_ca_id=None, stereo_ca_id=None, dh_id=None, inv_id=None):
        BaseObject.__init__(self)
        self._set_data(g_id, single_ca_id, stereo_ca_id, dh_id, inv_id)

    def _set_data(self, g_id=None, single_ca_id=None, stereo_ca_id=None, dh_id=None, inv_id=None):
        self.set_gid(g_id)
        self.set_single_id(single_ca_id)
        self.set_stereo_id(stereo_ca_id)
        self.set_dh_id(dh_id)
        self.set_inv_id(inv_id)

    def set_gid(self, id):
        if not GenerateData.is_exist_id(id):
            raise ObjectNotExist('enter generate data id is not exists')
        self.g_id = id

    def set_single_id(self, id):
        if id is not None and not SingleCalibration.is_exist_id(id):
            raise ObjectNotExist('enter single data id is not exists')
        self.single_ca_id = id

    def set_stereo_id(self, id):
        if id is not None and not StereoCalibration.is_exist_id(id):
            raise ObjectNotExist('enter stereo data id is not exists')
        self.stereo_ca_id = id

    def set_dh_id(self, id):
        if id is not None and not DH_Optimised.is_exist_id(id):
            raise ObjectNotExist('enter dh data id is not exists')
        self.dh_id = id

    def set_inv_id(self, id):
        if id is not None and not InverseTest.is_exist_id(id):
            raise ObjectNotExist('enter inv data id is not exists')
        self.inv_id = id

    def get_upload_path(self):
        return UPLOAD_FOLDER + str(self.id) + '/'

    def is_own_file(self, filename):
        return os.path.exists(UPLOAD_FOLDER + str(self.id) + '/' + filename)

    @classmethod
    def to_obj(cls, args_dict):
        for k in LocationList.__table__.columns:
            if k.name not in args_dict:
                args_dict[k.name] = None

        new_loc = LocationList( args_dict[LocationList.g_id.name],
                                args_dict[LocationList.single_ca_id.name],
                                args_dict[LocationList.stereo_ca_id.name],
                                args_dict[LocationList.dh_id.name],
                                args_dict[LocationList.inv_id.name]
                                )
        print(new_loc.__dict__)
        return new_loc

    @classmethod
    def update_obj(cls, args_dict):
        if LocationList.id.name not in args_dict:
            raise ObjectNotExist('LocationList id is wrong')
        loc = LocationList.get_by_id(args_dict[LocationList.id.name])
        if loc is None:
            raise ObjectNotExist('LocationList id is wrong')

        # add origin data which are not in req data
        for k in LocationList.__table__.columns:
            if k.name in args_dict:
                if k.name == LocationList.g_id.name:
                    loc.set_gid(args_dict[k.name])
                elif k.name == LocationList.single_ca_id.name:
                    loc.set_single_id(args_dict[k.name])
                elif k.name == LocationList.stereo_ca_id.name:
                    loc.set_stereo_id(args_dict[k.name])
                elif k.name == LocationList.dh_id.name:
                    loc.set_dh_id(args_dict[k.name])
                elif k.name == LocationList.inv_id.name:
                    loc.set_inv_id(args_dict[k.name])
        return loc
