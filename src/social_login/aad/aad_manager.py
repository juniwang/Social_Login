# -*- coding: utf-8 -*-

import sys
import urllib2
import urllib
import time

sys.path.append("..")

from social_login.util import *
from social_login.log import *

# Azure active directory (AAD)
class AadManager:
    token_url = safe_get_config("aad.token_url", "")
    api_url = safe_get_config("aad.api_url", "")
    api_version = safe_get_config("aad.api_version", "")

    client_id = safe_get_config("aad.client_id", "")
    client_secret = safe_get_config("aad.client_secret", "")
    access_token = ""
    token_expiration_time = ""

    def __init__(self):
        self.__get_access_token()

    def get_account_info(self, object_id):
        # object_id is the identity of an account.
        if not self.__check_access_token():
            return json.loads("{}")

        return self.__get_account_request(object_id)

    def __get_account_request(self, object_id):
        request_url = self.api_url + "/users/" + object_id + "?api-version=" + self.api_version
        try:
            req = urllib2.Request(request_url)
            req.add_header("Authorization", self.access_token)
            req.add_header("Content-Type", "application/json")

            response = urllib2.urlopen(req)
            response_json = json.loads(response.read())
            if not response_json.get("objectId", "") == "":
                return response_json
            return json.loads("{}")
        except Exception as e:
            log.error(e)
            return json.loads("{}")

    def create_account(self, principal_name, display_name, mail_nickname, password):
        # principal_name is not allow to be same for different accounts.
        # display_name and mail_nickname is necessary as parameters in the AAD graph api.
        if not self.__check_access_token():
            return ""

        data = {"accountEnabled": "true",
                "displayName": display_name,
                "mailNickname": mail_nickname,
                "passwordProfile": {
                    "password": password,
                    "forceChangePasswordNextLogin": "false"
                },
                "userPrincipalName": principal_name}

        return self.__create_account_request(data)

    def __create_account_request(self, data):
        # not responsible for checking available access_token and whether the account has existed.
        # objectId like "63eaf5a2-3978-4748-a486-9a0c2d2ad5b4" is the identity sequence of account.
        request_url = self.api_url + "/users?api-version=" + self.api_version
        try:
            req = urllib2.Request(request_url)
            req.add_header("Authorization", self.access_token)
            req.add_header("Content-Type", "application/json")
            json_data = json.dumps(data)
            req.add_data(json_data)

            response = urllib2.urlopen(req)
            response_json = json.loads(response.read())
            if not response_json.get("objectId", "") == "":
                return response_json.get("objectId", "")
            log.error(response_json["odata.error"]["message"]["value"])
            return ""
        except Exception as e:
            log.error(e)
            return ""

    def __get_access_token(self):
        # access_token is available in one hour, that is 3600s.
        data = {"grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret" : self.client_secret}
        try:
            req = urllib2.Request(self.token_url)
            post_data = urllib.urlencode(data)
            req.add_data(post_data)

            response = urllib2.urlopen(req)
            response_json = json.loads(response.read())
            if not response_json.get("access_token", "") == "":
                self.access_token = response_json.get("access_token", "")
                self.token_expiration_time = response_json.get("expires_on", "")
                return True
            log.error("fail to get AAD access_token: " + response_json.get("error", ""))
            return False
        except Exception as e:
            log.error("fail to get AAD access_token: " + e)
            return False

    def __check_access_token(self):
        try:
            if self.access_token == "" or int(self.token_expiration_time) <= int(time.time()):
                return self.__get_access_token()
            return True
        except Exception as e:
            log.error(e)
            return False



# below is test
#aad = AadManager()
#object_id = aad.create_account("A27", "lctestad.partner.onmschina.cn", "Test", "Test", "Test1234")
#print aad.get_account_info(object_id)

