# -*- coding: utf-8 -*-

import sys
import urllib2

sys.path.append("..")

import json
import requests
from requests.auth import HTTPBasicAuth

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

        state = "openhackathon"
        token_resp = get_remote(get_config("login.qq.access_token_url") + code + "&state=" + state)
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

    def get_user_info(self, token, uid):
        """Get weibo user info

        :type token: str
        :param token:

        :type uid: str
        :param uid:

        :rtype: dict
        :return:
            {"id":2330622122,"idstr":"2330622122","class":1,"screen_name":"test name","name":"test name",
            "province":"31","city":"10","location":"shanghai yangpu","description":"","url":"",
            "profile_image_url":"http://tp3.sinaimg.cn/2330622122/50/5629035320/1",
            "profile_url":"u/2330622122","domain":"","weihao":"","gender":"m","followers_count":34,
            "friends_count":42,"pagefriends_count":0,"statuses_count":0,"favourites_count":1,
            "created_at":"Mon Aug 22 17:58:15 +0800 2011","following":false,"allow_all_act_msg":false,
            "geo_enabled":true,"verified":false,"verified_type":-1,"remark":"","ptype":0,"allow_all_comment":true,
            "avatar_large":"http://tp3.sinaimg.cn/2330622122/180/5629035320/1","avatar_hd":"http://tp3.sinaimg.cn/2330622122/180/5629035320/1",
            "verified_reason":"","verified_trade":"","verified_reason_url":"","verified_source":"","verified_source_url":"",
            "follow_me":false,"online_status":0,"bi_followers_count":8,"lang":"zh-cn","star":0,"mbtype":0,"mbrank":0,
            "block_word":0,"block_app":0,"credit_score":80,"urank":6}
        """

        # https://api.weibo.com/2/users/show.json?access_token=2.005RDjXC0rYD8d39ca83156aLZWgZE&uid=1404376560
        user_info_resp = get_remote(get_config('login.weibo.user_info_url') + token + "&uid=" + uid)

        user_info = json.loads(user_info_resp)

        if user_info.get("error") is not None:
            raise Exception(user_info)

        return user_info



login_providers = {
    LOGIN_PROVIDER.WEIBO: WeiboLogin(),
    LOGIN_PROVIDER.QQ: QQLogin()
}
