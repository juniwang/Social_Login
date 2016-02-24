# -*- coding: utf-8 -*-

MYSQL_HOST = "localhost"
MYSQL_USER = "login_agent"
MYSQL_PWD = "login_agent"
MYSQL_DB = "login_agent"
MYSQL_PORT = 3306

Config = {
	"authentication" : "local",
    "mysql": {
        "connection": 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
    },
    "aad": {
        "token_url": "https://login.chinacloudapi.cn/6c5489bb-5bbc-4f81-bbbf-6c6e1f8c92ca/oauth2/token",
        "api_url": "https://graph.chinacloudapi.cn/6c5489bb-5bbc-4f81-bbbf-6c6e1f8c92ca",
        "api_version": "1.6",
        "client_id": "78cc7283-0254-47c4-aa07-ef924b1903b9",
        "client_secret": "OdTeIud/CYGYfvREvN6cd0LDwAHUWofAwDCUSuP2Bhc="
    },
    "identity_provider": {
        "github": {
            "user_info_url": 'https://api.github.com/user?access_token=',
            "emails_info_url": 'https://api.github.com/user/emails?access_token='
        },
        "qq": {
            "openid_url": 'https://graph.qq.com/oauth2.0/me?access_token=',
            "user_info_url": 'https://graph.qq.com/user/get_user_info?access_token=%s&oauth_consumer_key=%s&openid=%s'
        },
        "gitcafe": {
            "user_info_url": "https://gcas.dgz.sh/api/v1/user"
        },
        "weibo": {
            "user_info_url": 'https://api.weibo.com/2/users/show.json?access_token=',
            "email_info_url": 'https://api.weibo.com/2/account/profile/email.json?access_token='
        },
        "live": {
            "user_info_url": 'https://apis.live.net/v5.0/me?access_token='
        }
    }
}
