# -*- coding:utf-8 -*-
from SQLManager import sql_object
import logging
from SQLManager.SqlException import *
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class User(sql_object.Model, BaseObject):
    __tablename__ = 'User'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    account = sql_object.Column(sql_object.String(25), unique=True, nullable=False)

    password = sql_object.Column(sql_object.String(25), nullable=False)

    nickname = sql_object.Column(sql_object.String(32), unique=True, nullable=False)
    # icon_id = Column(Integer, unique=True, default=-1, ForeignKey('ICon.id'))

    @classmethod
    def is_exist(cls, db_obj):
        return False

    def __init__(self):
        BaseObject.__init__(self)
        # sql_object.__init__(self)
