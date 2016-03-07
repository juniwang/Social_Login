# -*- coding: utf-8 -*-

MYSQL_HOST = "localhost"
MYSQL_USER = "social_login"
MYSQL_PWD = "social_login"
MYSQL_DB = "social_login"
MYSQL_PORT = 3306

# NOTE: all following key/secrets for test purpose.
#HOSTNAME = "http://localhost"  # host name of the UI site
HOSTNAME = "http://open-hackathon-dev.chinacloudapp.cn"

QQ_CLIENT_ID = "101200890"
QQ_CLIENT_SECRET = "88ad67bd4521c4cc47136854781cb9b5"
QQ_META_CONTENT = "274307566465013314076545663016134754100636"

WEIBO_CLIENT_ID = "479757037"
WEIBO_CLIENT_SECRET = "efc5e75ff8891be37d90b4eaec5c02de"
WEIBO_META_CONTENT = "ae884e09bc02b700"

Config = {
    "mysql": {
        "connection": 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
    },
    "aad": {
        "default_domain": "lcaad.onmicrosoft.com",
        "default_password": "1qazXSW@",
        "token_url": "https://login.microsoftonline.com/e3de7a8d-0bd0-4287-90ee-aee57674cb55/oauth2/token",
        "api_url": "https://graph.windows.net/e3de7a8d-0bd0-4287-90ee-aee57674cb55",
        "api_version": "1.6",
        "client_id": "67d49d77-1cba-47fe-8703-7305c5869f35",
        "client_secret": "ybk03DgOUaEJqLRjXgfqgBqFFlevbNT/04t2Lik9528="
    },
    "adal": {
        "refresh_token_url": "https://login.windows.net/lcaad.onmicrosoft.com",
        "access_token_url": "https://login.windows.net/e3de7a8d-0bd0-4287-90ee-aee57674cb55"
    },
    "javascript": {
        "weibo": {
            "authorize_url": "https://api.weibo.com/oauth2/authorize?client_id=%s&redirect_uri=%s/weibo&scope=all" % (
                WEIBO_CLIENT_ID, HOSTNAME)
        },
        "qq": {
            "authorize_url": "https://graph.qq.com/oauth2.0/authorize?client_id=%s&redirect_uri=%s/qq&scope=get_user_info&response_type=code" % (
                QQ_CLIENT_ID, HOSTNAME)
        }
    },
    "login": {
        "qq": {
            "client_id": QQ_CLIENT_ID,
            "meta_content": QQ_META_CONTENT,
            "access_token_url": 'https://graph.qq.com/oauth2.0/token?grant_type=authorization_code&client_id=%s&client_secret=%s&redirect_uri=%s/qq&code=' % (
                QQ_CLIENT_ID, QQ_CLIENT_SECRET, HOSTNAME),
            "openid_url": 'https://graph.qq.com/oauth2.0/me?access_token=',
            "user_info_url": 'https://graph.qq.com/user/get_user_info?access_token=%s&oauth_consumer_key=%s&openid=%s'
        },
        "weibo": {
            "client_id": WEIBO_CLIENT_ID,
            "meta_content": WEIBO_META_CONTENT,
            "user_info_url": 'https://api.weibo.com/2/users/show.json?access_token=',
            "email_info_url": 'https://api.weibo.com/2/account/profile/email.json?access_token=',
            "access_token_url": 'https://api.weibo.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s/weibo&code=' % (
                WEIBO_CLIENT_ID, WEIBO_CLIENT_SECRET, HOSTNAME)
        }
    }
}
