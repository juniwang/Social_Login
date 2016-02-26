# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

from login_agent import *
from login_agent.constants import *
from login_agent.aad.aad_manager import AadManager
from login_agent.database.models import *

class LoginService():

    def __init__(self):
        self.aad_manager = AadManager()
        log.debug("login_service initializes successful!")

    def validate_request(self, redirect_url, authorized_id):
        # return True/False
        if safe_get_config("validate_developer", "disable") == ValidateDeveloper.ABLE:
            if not db_adapter.find_first_object_by(Developer, authorized_id=authorized_id, redirect_url=redirect_url):
                return False
        return True
