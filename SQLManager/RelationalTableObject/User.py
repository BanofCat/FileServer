# -*- coding:utf-8 -*-
from SQLManager import sql_object
from SQLManager.RelationalTableObject.BaseObject import BaseObject


class User(sql_object.Model, BaseObject):
    
    __tablename__ = 'User'

    id = sql_object.Column(sql_object.Integer, primary_key=True)

    account = sql_object.Column(sql_object.String(32), unique=True, nullable=False)

    password = sql_object.Column(sql_object.String(32), nullable=False)

    nickname = sql_object.Column(sql_object.String(32), unique=True, nullable=False)

    # icon_id = Column(Integer, unique=True, default=-1, ForeignKey('ICon.id'))

    @classmethod
    def is_exist(cls, db_obj):
        ret = User.query.filter(User.id == db_obj.id).first()
        if ret is None:
            return False
        return True

    def __init__(self, account, password, nickname):
        BaseObject.__init__(self)
        self._set_data(account, password, nickname)

    def _set_data(self, account, password, nickname):
        self.account = account
        self.password = password
        self.nickname = nickname
