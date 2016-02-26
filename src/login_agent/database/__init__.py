# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# noinspection PyUnresolvedReferences
from flask.ext.sqlalchemy import BaseQuery

from db_adapters import SQLAlchemyAdapter
from login_agent.util import safe_get_config

MYSQL_CONNECTION = 'mysql.connection'
DEFAULT_CONNECTION_URL = 'mysql://login_agent:login_agent@localhost/login_agent'

engine = create_engine(safe_get_config(MYSQL_CONNECTION, DEFAULT_CONNECTION_URL),
                       convert_unicode=True,
                       pool_size=50,
                       max_overflow=100,
                       echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property(BaseQuery)
db_adapter = SQLAlchemyAdapter(db_session)

from models import *

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)
