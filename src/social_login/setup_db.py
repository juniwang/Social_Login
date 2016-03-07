# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

from social_login.database import init_db

""" Type the following statement into mysql client.

create database social_login;
create User 'social_login'@'localhost' IDENTIFIED by 'social_login';
GRANT ALL on social_login.* TO 'social_login'@'localhost';
"""

init_db()