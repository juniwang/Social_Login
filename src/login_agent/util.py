# -*- coding: utf-8 -*-

import importlib
import json
import os
from datetime import datetime

from config import Config

def get_config(key):
    """Get configured value from configuration file according to specified key

    :type key: str or unicode
    :param key: the search key, separate section with '.'. For example: "mysql.connection"

    :Example:
        get_config("mysql.connection")

    :return configured value if specified key exists else None
    :rtype str or unicode or dict
    """
    ret = Config
    for arg in key.split("."):
        if arg in ret and isinstance(ret, dict):
            ret = ret[arg]
        else:
            return None
    return ret

def safe_get_config(key, default_value):
    """Get configured value from configuration file according to specified key and a default value

    :type key: str | unicode
    :param key: the search key, separate section with '.'. For example: "mysql.connection"

    :type default_value: object
    :param default_value: the default value if specified key cannot be found in configuration file

    :Example:
        safe_get_config("mysql.connection", "mysql://root:root@localhost:3306/db")

    :return configured value if specified key exists else the default value
    :rtype str or unicode or dict
    """
    r = get_config(key)
    return r if r else default_value

def get_now():
    """Return the current local date and time without tzinfo"""
    return datetime.utcnow()  # tzinfo=None


