# -*- coding:utf-8 -*-

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationship
from SQLManager import Base


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    account = Column(String(25), unique=True, nullable=False)
    password = Column(String(25), nullable=False)
    nickname = Column(String(32), unique=True, nullable=False)
    # icon_id = Column(Integer, unique=True, default=-1, ForeignKey('ICon.id'))



