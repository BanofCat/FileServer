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

        if g_id is not None and not GenerateData.is_exist_id(g_id):
            raise ObjectNotExist("Generate data table has not id: %d" % g_id)
        self.g_id = g_id
        self.single_ca_id = single_ca_id
        self.stereo_ca_id = stereo_ca_id
        self.dh_id = dh_id
        self.inv_id = inv_id

    def get_upload_path(self):
        return UPLOAD_FOLDER + str(self.id) + '/'
