import logging
import logging.config
from sqlalchemy.exc import SQLAlchemyError
from SQLManager import sql_object
import abc
from Exception.SqlException import DBException
import decimal
from datetime import datetime, date, time
from sqlalchemy.orm.dynamic import AppenderQuery
from flask_sqlalchemy import BaseQuery, DeclarativeMeta
from Configure.DB_Setting import *


class BaseObject(object):

    logging.config.fileConfig(LOG_CONFIG_FILE)
    logger = logging.getLogger(DB_LOGGER_NAME)
    logger.setLevel(logging.INFO)

    def __init__(self):
        pass

    @classmethod
    @abc.abstractmethod
    def is_exist(cls, db_obj):
        pass

    @classmethod
    def add(cls, db_obj, need_commit=False):
        cls.logger.info("in %s: add" % cls.__name__)
        if not isinstance(db_obj, sql_object.Model):
            cls.logger.error("add obj failed, %s is not a db model object" % db_obj)
            raise DBException
        is_exist = cls.is_exist(db_obj)
        if is_exist is True:
            cls.logger.error("db has a same object yet, can not add once more")
            # raise DBException
            return None
        sql_object.session.add(db_obj)
        if need_commit:
            try:
                sql_object.session.commit()
            except SQLAlchemyError as e:
                sql_object.session.rollback()
                cls.logger.error('commit failed : %s' % (str(e)))

    @classmethod
    def delete(cls, db_obj, need_commit=False):
        cls.logger.info("in %s: delete" % __name__)
        if not isinstance(db_obj, cls):
            cls.logger.error("delete obj failed, %s is not a kind of %s db model object" % (db_obj, __name__))
            raise DBException
        is_exist = cls.is_exist(db_obj)
        if not is_exist:
            cls.logger.error("db has not this object, can not delete a not exist obj")
            raise DBException

        sql_object.session.delete(db_obj)
        if need_commit:
            try:
                sql_object.session.commit()
            except SQLAlchemyError as e:
                sql_object.session.rollback()
                cls.logger.error('commit failed : %s' % (str(e)))

    @classmethod
    def commit(cls):
        cls.logger.info("in %s: commit" % __name__)
        try:
            sql_object.session.commit()
        except SQLAlchemyError as e:
            sql_object.session.rollback()
            cls.logger.error('commit failed : %s' % (str(e)))

    @classmethod
    def to_dict(cls, o):
        cls.logger.error('%s: to_dict' % __name__)
        if isinstance(o, list):
            obj_counter = 0
            obj_dict = {}
            for item in o:
                if isinstance(item, sql_object.Model):
                    obj_dict[item.__tablename__ + str(obj_counter)] = BaseObject.to_dict(item)
                    obj_counter += 1
                else:
                    cls.logger.error('can not recognize type: %s' % type(item))
            cls.logger.info("to_dict_list: ", obj_dict)
            return obj_dict
        elif isinstance(o.__class__, DeclarativeMeta):
            fields = {}
            counter = 0
            # for field in [x for x in dir(o) if not x.startswith('_') and x != 'metadata']:
            for field in o.__table__.columns:
                data = getattr(o, field.name)
                counter += 1

                if isinstance(data, datetime):
                    fields[field.name] = data.strftime("%Y-%m-%d %H:%M:%S.%F")[:-3]
                elif isinstance(data, date):
                    fields[field.name] = data.strftime("%Y-%m-%d")
                elif isinstance(data, time):
                    fields[field.name] = data.strftime("%H:%M:%S")
                elif isinstance(data, decimal.Decimal):
                    fields[field.name] = float(data)
                elif isinstance(data, BaseQuery):
                    pass
                elif isinstance(data, AppenderQuery):
                    pass
                elif isinstance(data, type):
                    pass
                elif isinstance(data, sql_object.Model):
                    pass
                elif isinstance(data, str):
                    fields[field.name] = data
                else:
                    fields[field.name] = BaseObject.to_dict(data)
            cls.logger.info("to_dict: ", fields)
            return fields
        return None
