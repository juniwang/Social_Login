# -*- coding: utf-8 -*-

import sys
import adal

sys.path.append("..")

from social_login import *
from social_login.constants import *
from social_login.aad.aad_manager import AadManager
from social_login.database.models import *

class LoginService():

    def __init__(self):
        self.aad_manager = AadManager()
        log.debug("login_service initializes successful!")

    def qq_login(self, open_id):
        self.get_aad_access_token(IDENTITY_PROVIDER.QQ, open_id)

    def weibo_login(self, user_id):
        self.get_aad_access_token(IDENTITY_PROVIDER.WEIBO, user_id)

    def get_aad_access_token(self, provider_name, open_id):
        # return str or None
        account_info = self.get_aad_account_username_password(provider_name, open_id)
        if not account_info:
            return None

        try:
            token_response = adal.acquire_token_with_username_password(safe_get_config("adal.refresh_token_url", ""),
                                                                       str(account_info["username"]),
                                                                       str(account_info["password"]))

            refresh_token = str(token_response['refreshToken'])
            token_response = adal.acquire_token_with_refresh_token(safe_get_config('adal.access_token_url', ""), refresh_token)
            return str(token_response["accessToken"])
        except Exception as e:
            log.error("fail to get access token")
            return None

    def get_aad_account_username_password(self, provider_name, open_id):
        """
        :param provider_name: define in the IdentityProvider constants.
        :param open_id: open_id to identity the user by QQ or Weibo.
        :return: Dict or None
        """
        account = db_adapter.find_first_object_by(Account, open_id = open_id)
        if account:
            return {"username": account.aad_principal_name, "password": account.aad_password}
        else:
            account = self.__create_aad_account(provider_name, open_id)
            if not account:
                log.error("fail to create new AAD account")
                return None
            return {"username": account.aad_principal_name, "password": account.aad_password}


    def __create_aad_account(self, provider_name, open_id):
        # return None or Account
        principle_name = self.__generate_principal_name(provider_name, open_id)
        display_name = self.__generate_display_name(provider_name, open_id)
        mail_nickname = self.__generate_mail_nickname(provider_name, open_id)
        password = self.__generate_password(provider_name, open_id)

        object_id = self.aad_manager.create_account(principle_name, display_name, mail_nickname, password)
        if object_id == "":
            return None
        return db_adapter.add_object_kwargs(Account,
                                            open_id = open_id,
                                            identity_provider = provider_name,
                                            aad_object_id = object_id,
                                            aad_principal_name = principle_name,
                                            aad_password = password,
                                            aad_display_name = display_name,
                                            aad_mail_nickname = mail_nickname)

    def __generate_principal_name(self, provider_name, open_id):
        return provider_name + open_id + "@" + self.__get_domain_name()

    def __get_domain_name(self):
        if not hasattr(self, "domain"):
            self.domain = safe_get_config("aad.default_domain", "")
        return self.domain

    def __generate_display_name(self, provider_name, open_id):
        # display_name could be same for different accounts.
        return provider_name + open_id

    def __generate_mail_nickname(self, provider_name, open_id):
        # mail_nickname could be same for different accounts.
        return provider_name + open_id

    def __generate_password(self, provider_name, open_id):
        if not hasattr(self, "password"):
            self.password = safe_get_config("aad.default_password", "")
        return self.password


#test
#token_response = adal.acquire_token_with_username_password(
#		'https://login.windows.net/lcaad.onmicrosoft.com',
#                'qq1112234335@lcaad.onmicrosoft.com',
#                '1qazXSW@')

#print token_response