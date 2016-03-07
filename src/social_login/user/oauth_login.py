# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

from social_login import *
from social_login.constants import *


class LoginBase():
    def login(self, args):
        pass

class QQLogin(LoginBase):

    def get_token(self, code):
        """ Get qq access token

        :type code: str
        :param code:

        :rtype: str
        :return: access token
        """

        token_resp = get_remote(get_config("login.qq.access_token_url") + code)
        if token_resp.find('callback') == 0:
            error = json.loads(token_resp[10:-4])
            raise Exception(error)

        query = qs_dict(token_resp)
        return query["access_token"]

    def get_info(self, token):
        """ Get qq open id

        :type token: str
        :param token:

        :rtype: dict
        :return: info
        """

        openid_resp = get_remote(get_config("login.qq.openid_url") + token)
        log.debug("get access_token from qq:" + token)
        info = json.loads(openid_resp[10:-4])

        if info.get("error") is not None:
            raise Exception(info)

        return info

class WeiboLogin(LoginBase):

    def get_token(self, code):
        """ Get weibo access token

        :type code: str
        :param code:

        :rtype: dict
        :return: access token and uid
        """

        token_resp = post_to_remote(get_config('login.weibo.access_token_url') + code, {})
        if token_resp.get("error") is not None:
            raise Exception(token_resp)

        return token_resp

login_providers = {
    LOGIN_PROVIDER.WEIBO: WeiboLogin(),
    LOGIN_PROVIDER.QQ: QQLogin()
}
