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



class GithubLogin(LoginBase):
    """Sign in with github

    :Example:
        from client.user.login import GithubLogin

        GithubLogin()

    .. notes::
    """

    def login(self, args):
        """ github Login

        :type args: dict
        :param args:

        :rtype: dict
        :return: token and instance of user
        """

        log.info('login from GitHub')
        code = args.get('code')
        if not code:
            return None

        access_token = self.get_token(code)
        user_info = self.get_user_info(access_token)
        email_list = self.get_emails(access_token)

        name = user_info["login"]
        nickname = name
        if "name" in user_info:
            nickname = user_info["name"]
        if not nickname:
            nickname = name

        required_info = {
            "openid": str(user_info["id"]),
            "provider": LOGIN_PROVIDER.GITHUB,
            "name": name,
            "nickname": nickname,
            "access_token": access_token,
            "email_list": email_list,
            "avatar_url": user_info["avatar_url"]
        }

        return required_info

    def get_token(self, code):
        """ Get github access token

        :type code: str
        :param code:

        :rtype: str
        :return: access token
        """

        token_resp = get_remote(get_config('login.github.access_token_url') + str(code))
        query = qs_dict(token_resp)
        if query.get("error") is not None:
            raise Exception(query)

        return query["access_token"]

    def get_emails(self, token):
        """Get user primary email

        :type token: str
        :param token:

        :rtype: dict
        :return: emails
        """
        email_info_resp = get_remote(get_config('login.github.emails_info_url') + token)
        email_list = json.loads(email_info_resp)

        return email_list

    def get_user_info(self, token):
        """Get qq user info

        :type token: str
        :param token:

        :rtype: dict
        :return:
            "url":"https://api.github.com/users/juniwang","html_url":"https://github.com/juniwang",
            "followers_url":"https://api.github.com/users/juniwang/followers",        log.debug("get admin user info from " + provider + " : "  + user_info_resp + '\n' )

            "following_url":"https://api.github.com/users/juniwang/following{/other_user}",
            "starred_url":"https://api.github.com/users/juniwang/starred{/owner}{/repo}",
            "gists_url":"https://api.github.com/users/juniwang/gists{/gist_id}",
            "events_url":"https://api.github.com/users/juniwang/events{/privacy}",
            {"login":"juniwang","id":8814383,"avatar_url":"https://avatars.githubusercontent.com/u/8814383?v=3","gravatar_id":"",
            "subscriptions_url":"https://api.github.com/users/juniwang/subscriptions",
            "received_events_url":"https://api.github.com/users/juniwang/received_events","type":"User","site_admin":false,
            "name":"Junbo Wang","company":"","blog":"","location":"Shanghai China",
            "organizations_url":"https://api.github.com/users/juniwang/orgs","repos_url":"https://api.github.com/users/juniwang/repos",

            "email":"wangjunbo924@gmail.com","hireable":false,"bio":null,"public_repos":12,"public_gists":0,"followers":0,
            "following":1,"created_at":"2014-09-18T01:30:30Z","updated_at":"2014-11-25T09:00:37Z","private_gists":0,
            "plan":{"name":"free","space":307200,"collaborators":0,"private_repos":0}}
            "total_private_repos":0,"owned_private_repos":0,"disk_usage":14179,"collaborators":0,

        """
        user_info_resp = get_remote(get_config('login.github.user_info_url') + token)

        user_info = json.loads(user_info_resp)
        if user_info.get("message") is not None:
            raise Exception(user_info)

        return user_info


class GitcafeLogin(LoginBase):
    """Sign in with gitcafe

    :Example:
        from client.user.login import GitcafeLogin

        GitcafeLogin()

    .. notes::
    """

    def login(self, args):
        """ gitcafe Login

        :type args: dict
        :param args:

        :rtype: dict
        :return: token and instance of user
        """

        log.info('login from Gitcafe')
        code = args.get('code')
        if not code:
            return None

        access_token = self.get_token(code)
        user_info = self.get_user_info("Bearer " + access_token)

        name = user_info['username']
        email = user_info['email']
        nickname = user_info['fullname']
        if nickname is None:
            nickname = name

        if user_info['avatar_url'].startswith('https'):
            avatar_url = user_info['avatar_url']
        else:
            avatar_url = "https" + user_info['avatar_url'][4:]

        email_list = [
            {
                'name': name,
                'email': email,
                'verified': 1,
                'primary': 1
            }
        ]

        required_info = {
            "openid": user_info['id'],
            "provider": LOGIN_PROVIDER.GITCAFE,
            "name": name,
            "nickname": nickname,
            "access_token": access_token,
            "email_list": email_list,
            "avatar_url": avatar_url
        }

        return required_info

    def get_token(self, code):
        """ Get gitcafe access token

        :type code: str
        :param code:

        :rtype: str
        :return: access token
        """
        token_resp = get_remote(get_config("login.gitcafe.access_token_url") + code)
        query = qs_dict(token_resp)
        if query.get("error") is not None:
            raise Exception(query)

        return query["access_token"]

    def get_user_info(self, authorization):
        """Get qq user info

        :type authorization: str
        :param authorization:

        :rtype: dict
        :return: user info
        """
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        request = urllib2.Request(get_config("login.gitcafe.user_info_url"))
        request.add_header("Authorization", authorization)
        user_info = json.loads(opener.open(request).read())

        if user_info.get("error") is not None:
            raise Exception(user_info)

        return user_info


class WeiboLogin(LoginBase):
    """Sign in with weibo

    :Example:
        from client.user.login import WeiboLogin

        WeiboLogin()

    .. notes::
    """

    def login(self, args):
        """ weibo Login

        :type args: dict
        :param args:

        :rtype: dict
        :return: token and instance of user
        """

        log.info("login from Weibo Sina")
        code = args.get("code")
        if not code:
            return None

        access_token = self.get_token(code)
        user_info = self.get_user_info(access_token["access_token"], access_token["uid"])

        # Get email need to apply high-level interface
        # email = self.get_email(access_token["access_token"], access_token["uid"])

        name = user_info["name"]
        email_list = [
            {
                'name': name,
                'email': '',
                'verified': 1,
                'primary': 1
            }
        ]

        required_info = {
            "openid": str(user_info["id"]),
            "provider": LOGIN_PROVIDER.WEIBO,
            "name": name,
            "nickname": user_info["screen_name"],
            "access_token": access_token["access_token"],
            "email_list": email_list,
            "avatar_url": user_info["avatar_hd"]
        }

        return required_info

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

    def get_email(self, token, uid):
        """Get weibo user info

        :type token: str
        :param token:

        :rtype: str
        :return : email
        """

        email_info_resp = get_remote(get_config('login.weibo.email_info_url') + token)
        email_info_resp_json = json.loads(email_info_resp)

        if email_info_resp_json.get("error") is not None:
            raise Exception(email_info_resp_json)

        return email_info_resp_json['email']


class LiveLogin(LoginBase):
    """Sign in with live

    :Example:
        from client.user.login import LiveLogin

        LiveLogin()

    .. notes::
    """

    def login(self, args):
        """ live Login

        :type args: dict
        :param args:

        :rtype: dict
        :return: token and instance of user
        """

        log.info('login from  Live')
        code = args.get('code')
        if not code:
            return None

        access_token = self.get_token(code)
        user_info = self.get_user_info(access_token)

        name = user_info["name"]
        email = user_info["emails"]["account"]
        email_list = [
            {
                'name': name,
                'email': email,
                'verified': 1,
                'primary': 1
            }
        ]

        required_info = {
            "openid": user_info["id"],
            "provider": LOGIN_PROVIDER.LIVE,
            "name": name,
            "nickname": name,
            "access_token": access_token,
            "email_list": email_list,
            "avatar_url": None
        }

        return required_info

    def get_token(self, code):
        """ Get live access token

        :type code: str
        :param code:

        :rtype: str
        :return: access token and uid
        """

        # live need post a form to get token
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {
            'client_id': get_config('login.live.client_id'),
            'client_secret': get_config('login.live.client_secret'),
            'redirect_uri': get_config('login.live.redirect_uri'),
            'grant_type': 'authorization_code',
            'code': code
        }
        # Following is use urllib to post request
        url = get_config('login.live.access_token_url')
        r = requests.post(url, data=data, headers=headers)
        resp = r.json()

        if resp.get("error") is not None:
            raise Exception(resp)

        return resp["access_token"]

    def get_user_info(self, token):
        """Get live user info

        :type token: str
        :param token:

        :rtype: dict
        :return:
            {'first_name': 'Ice', 'last_name': 'Shi', 'name': 'Ice Shi', 'locale': 'en_US',
            'gender': None,
            'emails': {'personal': None, 'account': 'iceshi@outlook.com', 'business': None, 'preferred': 'iceshi@outlook.com'},
            'link': 'https://profile.live.com/',
            'updated_time': '2015-05-13T02:28:32+0000',
            'id': '655c03b1b314b5ee'}
        """

        user_info_resp = get_remote(get_config('login.live.user_info_url') + token)
        user_info = json.loads(user_info_resp)

        if user_info.get("error") is not None:
            raise Exception(user_info)

        return user_info


class AlaudaLogin(LoginBase):
    """Sign in with alauda account

    ### 步骤四：客户端根据code请求 Token
        #### 参数
        | name         | value              |      |
        |--------------+--------------------+------|
        | grant_type   | authorization_code |  必选 |
        | code         |  上一步获得的code     | 必选  |
        | redirect_uri |  重定向URI           | 必选  |
        | client_id    |  客户端ID            | 必选  |
        ### 认证方式
        灵云雀
        Basic Auth:
             username：client_id
             password: client_secret
        #### 举例
        `
        POST /token HTTP/1.1
        Host: server.example.com
        Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
        Content-Type: application/x-www-form-urlencoded

        grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
        &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb
    """

    def login(self, args):
        code = args.get('code')
        if not code:
            return None

        log.info('login from alauda, code = ' + code)

        # basic auth header, content_type and post data
        client_id = get_config("login.alauda.client_id")
        client_secret = get_config("login.alauda.client_secret")
        basic_auth = HTTPBasicAuth(client_id, client_secret)

        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': get_config('login.alauda.redirect_uri'),
            'client_id': client_id
        }

        # Post request
        url = get_config('login.alauda.access_token_url')
        r = requests.post(url, data=data, headers=headers, auth=basic_auth)
        resp = r.json()

        # {u'username': u'junbowang', u'realname': u'junbowang', u'success': True,
        # u'access_token': u'3MyZLF8RVo5X8lDLZQSj5s4OpIGQGn', u'token_type': u'Bearer',
        # u'logo_file': u'/static/images/user/default-logo.png', u'email': u'juniwang@microsoft.com'}
        if not resp.get("success"):
            log.debug("get access token failed from alauda: %r" % resp)
            return None

        # username will used as openid too since its unique. And also it's the 'namespace' for user's alauda resource
        username = resp["username"]
        email = resp["email"]
        email_list = [
            {
                'name': username,
                'email': email,
                'verified': 1,
                'primary': 1
            }
        ]

        required_info = {
            "openid": username,
            "provider": LOGIN_PROVIDER.ALAUDA,
            "name": username,
            "nickname": resp.get("realname", username),
            "access_token": resp["access_token"],
            "email_list": email_list,
            "avatar_url": resp.get("logo_file"),
            "oxford_api": resp.get("oxford_api")
        }

        return required_info


login_providers = {
    LOGIN_PROVIDER.GITHUB: GithubLogin(),
    LOGIN_PROVIDER.WEIBO: WeiboLogin(),
    LOGIN_PROVIDER.QQ: QQLogin(),
    LOGIN_PROVIDER.GITCAFE: GitcafeLogin(),
    LOGIN_PROVIDER.ALAUDA: AlaudaLogin(),
    LOGIN_PROVIDER.LIVE: LiveLogin()
}
