# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class LocationList(sql_object.Model, BaseObject):

    __tablename__ = 'LocationList'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    g_id = sql_object.relationship(
        "GenerateData",
        backref='LocationList',
        lazy='dynamic',
        nullable=True
    )

    single_ca_id = sql_object.relationship(
        "SingleCalibration",
        backref='LocationList',
        lazy='dynamic',
        nullable=True
    )

    stereo_ca_id = sql_object.relationship(
        "StereoCalibration",
        backref='LocationList',
        lazy='dynamic',
        nullable=True
    )

    dh_id = sql_object.relationship(
        "DH_Optimised",
        backref='LocationList',
        lazy='dynamic',
        nullable=True
    )

    inv_id = sql_object.relationship(
        "InverseTest",
        backref='LocationList',
        lazy='dynamic',
        nullable=True
    )

    @classmethod
    def is_exist(cls, db_obj):
        ret = LocationList.query.filter(LocationList.id == db_obj.id).first()
        if ret is None:
            return False
        return True

    def __init__(self, id, g_id=None, single_ca_id=None, stereo_ca_id=None, dh_id=None, inv_id=None):
        BaseObject.__init__(self)
        self._set_data(id, g_id, single_ca_id, stereo_ca_id, dh_id, inv_id)

    def _set_data(self, id, g_id=None, single_ca_id=None, stereo_ca_id=None, dh_id=None, inv_id=None):

        self.id = id
        self.g_id = g_id
        self.single_ca_id = single_ca_id
        self.stereo_ca_id = stereo_ca_id
        self.dh_id = dh_id
        self.inv_id = inv_id
