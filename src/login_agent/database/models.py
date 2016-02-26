# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, TypeDecorator
from sqlalchemy.orm import backref, relation
from . import Base, db_adapter
from datetime import datetime
from login_agent.util import get_now
import json
from pytz import utc
from dateutil import parser


def relationship(*arg, **kw):
    ret = relation(*arg, **kw)
    db_adapter.commit()
    return ret


def date_serializer(date):
    return long((date - datetime(1970, 1, 1)).total_seconds() * 1000)


def to_dic(inst, cls):
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    convert = dict()
    convert[TZDateTime] = date_serializer

    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type.__class__ in convert.keys() and v is not None:
            try:
                func = convert[c.type.__class__]
                d[c.name] = func(v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type.__class__])
        else:
            d[c.name] = v
    return d


def to_json(inst, cls):
    return json.dumps(to_dic(inst, cls))


class TZDateTime(TypeDecorator):
    '''
        usage: remove datetime's tzinfo
        To set all datetime datas are the naive datetime (tzinfo=None) in the whole environment
    '''

    impl = DateTime

    def process_bind_param(self, value, dialect):
        if value is not None:
            if isinstance(value, basestring) or isinstance(value, str):
                value = parser.parse(value)
            if isinstance(value, datetime):
                if value.tzinfo is not None:
                    value = value.astimezone(utc)
                    value.replace(tzinfo=None)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            if isinstance(value, datetime):
                if value.tzinfo is not None:
                    value = value.astimezone(utc)
                    value.replace(tzinfo=None)
        return value


class DBBase(Base):
    """
    DB model base class, providing basic functions
    """
    __abstract__ = True

    def __init__(self, **kwargs):
        super(DBBase, self).__init__(**kwargs)

    def dic(self):
        return to_dic(self, self.__class__)

    def json(self):
        return to_json(self, self.__class__)

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, self.json())


class Developer(DBBase):
    # users like companies or developers who use our login service.
    __tablename__ = 'developer'

    id = Column(Integer, primary_key=True)
    authorized_id = Column(String(50))
    name = Column(String(50))
    password = Column(String(100))  # encrypted password for the default admin/guest users.

    nickname = Column(String(50))
    email = Column(String(20))
    avatar_url = Column(String(200))
    domain = Column(String(50))
    create_time = Column(TZDateTime, default=get_now())
    redirect_url = Column(String(100))
    html_url = Column(String(100))

    def __init__(self, **kwargs):
        super(Developer, self).__init__(**kwargs)


class Account(DBBase):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    open_id = Column(String(100)) # open_id is given by the identity_provider
    identity_provider = Column(String(30))
    object_id = Column(String(50)) # object_id is the identity of aad
    developer_id = Column(Integer, ForeignKey("developer.id"))

    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)

class LocalAccount(DBBase):
    __tablename__ = 'local_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(100))
    nickname = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    address = Column(String(50))
    nation = Column(String(20))

    def __init__(self, **kwargs):
        super(LocalAccount, self).__init__(**kwargs)


class OauthParameter(DBBase):
    __tablename__ = "oauth_parameter"

    id = Column(Integer, primary_key=True)
    identity_provider = Column(String(30))
    app_id = Column(String(100))
    app_secret = Column(String(100))
    redirect_url = Column(String(100))
    developer_id = Column(Integer, ForeignKey("developer.id"))
    rule = Column(String(50))

    def __init__(self, **kwargs):
        super(OauthParameter, self).__init__(**kwargs)