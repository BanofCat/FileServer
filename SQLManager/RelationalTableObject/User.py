# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject
from werkzeug.security import generate_password_hash, check_password_hash
from Configure.HttpSetting import *


class User(sql_object.Model, BaseObject):
    
    __tablename__ = 'User'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    account = sql_object.Column(sql_object.String(32), unique=True, nullable=False)

    password = sql_object.Column(sql_object.String(128), nullable=False)

    nickname = sql_object.Column(sql_object.String(32), unique=True, nullable=False)

    # icon_id = Column(Integer, unique=True, default=-1, ForeignKey('ICon.id'))

    def __init__(self, account, password, nickname):
        BaseObject.__init__(self)
        self._set_data(account, password, nickname)

    def _set_data(self, account, password, nickname):
        self.account = account
        self.set_password(password)
        self.nickname = nickname

    def check_password(self, password):
        return check_password_hash(self.password,  password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        return True

    @classmethod
    def is_exist(cls, db_obj):
        id_ret = cls.query.filter(cls.id == db_obj.id).first()
        acc_ret = cls.query.filter(cls.account == db_obj.account).first()
        if id_ret is None and acc_ret is None:
            print("false----: %s" % db_obj.id)
            return False
        print("true----: %s" % db_obj.id)
        return True

    @classmethod
    def get_by_account(cls, account):
        return cls.query.filter(cls.account == account).first()

    @classmethod
    def get_by_nickname(cls, nickname):
        return cls.query.filter(cls.nickname == nickname).first()

    def to_dict(self, obj):
        pass


    @classmethod
    def to_obj(cls, package):
        dict_package = eval(package)
        print(">>>>>>", dict_package)
        # if isinstance(obj_class, User):
        req_msg = dict_package[OBJECT_DATA_N]
        new_obj = User(req_msg[ACCOUNT_N], req_msg[PASSWORD_N], req_msg[NICKNAME_N])
        print(new_obj.id, new_obj.account, new_obj.password, new_obj.nickname)
        return new_obj


