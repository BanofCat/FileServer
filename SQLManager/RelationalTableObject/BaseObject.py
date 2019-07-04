from SQLManager import sql_object
import logging
from SQLManager.SqlException import *
from sqlalchemy.exc import SQLAlchemyError


class BaseObject(sql_object.Model):

    __tablename__ = 'BaseObject'

    id = sql_object.Column(sql_object.Integer, unique=True, nullable=False)

    obj_logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    @classmethod
    def add(cls, db_obj, need_commit=False):
        if not isinstance(db_obj, cls):
            cls.obj_logger.error("add obj failed, %s is not a db model object" % (db_obj, __name__))
            raise DBException
        is_exist = cls.query.filter(cls.id == db_obj.id).one()
        if is_exist is not None:
            cls.obj_logger.error("db has a same object, can not add more")
            raise DBException
        sql_object.session.add(db_obj)
        if need_commit:
            try:
                sql_object.session.commit()
            except SQLAlchemyError as e:
                sql_object.session.rollback()
                cls.obj_logger.error('commit failed : %s' % (tr(e)))
                raise SQLException

    @classmethod
    def delete(cls, db_obj, need_commit=False):
        if not isinstance(db_obj, cls):
            cls.obj_logger.error("delete obj failed, %s is not a kind of %s db model object" % (db_obj, __name__))
            raise DBException
        is_exist = cls.query.filter(cls.id == db_obj.id).one()
        if is_exist is None:
            cls.obj_logger.error("db has not this object, can not delete a not exist obj")
            raise DBException

        sql_object.session.delete(db_obj)
        if need_commit:
            try:
                sql_object.session.commit()
            except SQLAlchemyError as e:
                sql_object.session.rollback()
                cls.obj_logger.error('commit failed : %s' % (str(e)))
                raise SQLException

    @classmethod
    def commit(cls):
        try:
            sql_object.session.commit()
        except SQLAlchemyError as e:
            sql_object.session.rollback()
            cls.obj_logger.error('commit failed : %s' % (str(e)))
            raise SQLException
