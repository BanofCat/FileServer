from SQLManager import sql_object
import logging
from SQLManager.Exception.SqlException import *
from sqlalchemy.exc import SQLAlchemyError
import abc


class BaseObject(object):
    pass

    # __tablename__ = 'BaseObject'

    # id = sql_object.Column(sql_object.Integer, unique=True, nullable=False, primary_key=True)
    #
    obj_logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    @classmethod
    @abc.abstractmethod
    def is_exist(cls, db_obj):
        pass

    @classmethod
    def add(cls, db_obj, need_commit=False):
        print("in %s add" % __name__)
        if not isinstance(db_obj, sql_object.Model):
            cls.obj_logger.error("add obj failed, %s is not a db model object" % db_obj)
            raise DBException
        is_exist = cls.is_exist(db_obj)
        if is_exist:
            cls.obj_logger.error("db has a same object, can not add once more")
            raise DBException
        sql_object.session.add(db_obj)
        if need_commit:
            try:
                sql_object.session.commit()
            except SQLAlchemyError as e:
                sql_object.session.rollback()
                cls.obj_logger.error('commit failed : %s' % (str(e)))
                print('Test: commit failed')

    @classmethod
    def delete(cls, db_obj, need_commit=False):
        print("in %s delete" % __name__)
        if not isinstance(db_obj, cls):
            cls.obj_logger.error("delete obj failed, %s is not a kind of %s db model object" % (db_obj, __name__))
            raise DBException
        is_exist = cls.is_exist(db_obj)
        if not is_exist:
            cls.obj_logger.error("db has not this object, can not delete a not exist obj")
            raise DBException

        sql_object.session.delete(db_obj)
        if need_commit:
            try:
                sql_object.session.commit()
            except SQLAlchemyError as e:
                sql_object.session.rollback()
                cls.obj_logger.error('commit failed : %s' % (str(e)))
                print('Test: commit failed')

    @classmethod
    def commit(cls):
        print("in %s commit" % __name__)
        try:
            sql_object.session.commit()
        except SQLAlchemyError as e:
            sql_object.session.rollback()
            cls.obj_logger.error('commit failed : %s' % (str(e)))
            print("Test: commit failed")
