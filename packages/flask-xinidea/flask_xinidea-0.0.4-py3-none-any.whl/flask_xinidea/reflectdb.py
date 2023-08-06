#

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative.api import DeclarativeMeta


class ReflectDB(object):
    def __init__(self, bind, app=None):
        if app and bind in app.config['SQLALCHEMY_BINDS']:
            self.__bind = app.config['SQLALCHEMY_BINDS'][bind]
        else:
            self.__bind = bind
        self.__Base = automap_base()
        self.__engine = create_engine(
            self.__bind, pool_size=10, pool_recycle=7200, pool_pre_ping=True, encoding='utf-8')
        self.__Base.prepare(self.__engine, reflect=True)
        self.__tables = self.__Base.classes
        self.session = Session(self.__engine)

    def get_table(self, table):
        if hasattr(self.__tables, table):
            t = getattr(self.__tables, table)
            if isinstance(t, DeclarativeMeta):
                t.query = self.session.query(t)
                return t
        raise TypeError(
            f'{table} is invalid table name or {table} table not exists')
