# -*- coding: utf-8 -*-

MYSQL_HOST = "localhost"
MYSQL_USER = "login_agent"
MYSQL_PWD = "login_agent"
MYSQL_DB = "login_agent"
MYSQL_PORT = 3306

# NOTE: all following key/secrets for test purpose.
#HOSTNAME = "http://localhost"  # host name of the UI site
HOSTNAME = "http://open-hackathon-dev.chinacloudapp.cn"

QQ_OAUTH_STATE = "openhackathon"  # todo state should be constant. Actually it should be unguessable to prevent CSFA
HACKATHON_API_ENDPOINT = "http://localhost:15000"

# github key for `localhost`
GITHUB_CLIENT_ID = "b44f3d47bdeb26b9c4e6"
GITHUB_CLIENT_SECRET = "98de14161c4b2ed3ea7a19787d62cda73b8e292c"

QQ_CLIENT_ID = "101200890"
QQ_CLIENT_SECRET = "88ad67bd4521c4cc47136854781cb9b5"
QQ_META_CONTENT = "274307566465013314076545663016134754100636"

# gitcafe domain:  gcas.dgz.sh/gcs.dgz.sh for Staging, api.gitcafe.com/gitcafe.com for Production
GITCAFE_CLIENT_ID = "1c33ecdf4dd0826325f60a92e91834522b1cdf47a7f90bdaa79f0526fdc48727"
GITCAFE_CLIENT_SECRET = "80b63609000b20c1260df28081c08712617648e1b528086bbb089f0af4614509"

WEIBO_CLIENT_ID = "479757037"
WEIBO_CLIENT_SECRET = "efc5e75ff8891be37d90b4eaec5c02de"
WEIBO_META_CONTENT = "ae884e09bc02b700"

LIVE_CLIENT_ID = "000000004414E0A6"
LIVE_CLIENT_SECRET = "b4mkfVqjtwHY2wJh0T4tj74lxM5LgAT2"

ALAUDA_CLIENT_ID = "4VR9kzNZVyWcnk9OnAwMuSus7xOOcozJIpic6W6y"
ALAUDA_CLIENT_SECRET = "E5PUL5h9feLlEirec5HQhjIzYecv7vVbEBjWLBkRMoCoFXdvS1PzNmd4AAeNgu4M2AJ87uGnnJaoDLCcDuVxkBoHRWCn6LmfB4SKK1Dty1SkGukkTcZPEk9wpHLSiRQ3"

Config = {
	"validate_developer" : "disable",
    "mysql": {
        "connection": 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)
    },
    "aad": {
        "default_domain": "lctestad.partner.onmschina.cn",
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
    },
    "javascript": {
        "github": {
            "authorize_url": "https://github.com/login/oauth/authorize?client_id=%s&redirect_uri=%s/github&scope=user" % (
                GITHUB_CLIENT_ID, HOSTNAME)
        },
        "weibo": {
            "authorize_url": "https://api.weibo.com/oauth2/authorize?client_id=%s&redirect_uri=%s/weibo&scope=all" % (
                WEIBO_CLIENT_ID, HOSTNAME)
        },
        "qq": {
            "authorize_url": "https://graph.qq.com/oauth2.0/authorize?client_id=%s&redirect_uri=%s/qq&scope=get_user_info&state=%s&response_type=code" % (
                QQ_CLIENT_ID, HOSTNAME, QQ_OAUTH_STATE)
        },
        "gitcafe": {
            "authorize_url": "https://gcs.dgz.sh/oauth/authorize?response_type=code&client_id=%s&redirect_uri=%s/gitcafe&scope=public" % (
                GITCAFE_CLIENT_ID, HOSTNAME)
        },
        "live": {
            "authorize_url": "https://login.live.com/oauth20_authorize.srf?client_id=%s&scope=wl.basic+,wl.emails&response_type=code&redirect_uri=%s/live" % (
                LIVE_CLIENT_ID, HOSTNAME)
        },
        "alauda": {
            "authorize_url": "http://console.int.alauda.io/oauth/authorize?response_type=code&client_id=%s&state=state&redirect_uri=%s/alauda" % (
                ALAUDA_CLIENT_ID, HOSTNAME)
        }
    }
}
