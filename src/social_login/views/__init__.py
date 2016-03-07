# -*- coding: utf-8 -*-

import sys

sys.path.append("..")

from flask import Response, render_template, request, g, redirect, make_response, session, url_for, abort
from flask_login import login_user

from social_login.service.login_service import *
from social_login.user.oauth_login import *



def render(template_name_or_list, **context):
    log.debug("rendering template '%s'" % (template_name_or_list))
    return render_template(template_name_or_list, **context)

@app.errorhandler(401)
def custom_401(e):
    return render("error.html", message="401"), 401

@app.errorhandler(404)
def page_not_found(e):
    return render('error.html', message="404"), 404

@app.route("/")
@app.route("/login")
def login():
    return render("login.html")

# js config
@app.route('/config.js')
def js_config():
    resp = Response(response="var CONFIG=%s" % json.dumps(get_config("javascript")),
                    status=200,
                    mimetype="application/javascript")
    return resp


@app.route("/qq")
def qq_login():
    code = request.args.get("code", "")

    service = LoginService()
    qq_login = QQLogin()

    # get QQ access_token
    social_access_token = qq_login.get_token(code)
    user_info = qq_login.get_info(social_access_token)
    openid = user_info["openid"]
    aad_access_token = service.get_aad_access_token(LOGIN_PROVIDER.QQ, openid)

    return __login(LOGIN_PROVIDER.QQ, social_access_token, aad_access_token)


@app.route('/weibo')
def weibo_login():
    code = request.args.get("code", "")

    service = LoginService()
    weibo_login = WeiboLogin()

    response = weibo_login.get_token(code)
    id = response["uid"]
    aad_access_token = service.get_aad_access_token(LOGIN_PROVIDER.WEIBO, id)

    return __login(LOGIN_PROVIDER.WEIBO, response["access_token"], aad_access_token)


def __login(provider, social_access_token, aad_access_token):
    try:
        log.info("login successfully:")

        if session.get("return_url") is not None:
            resp = make_response(redirect(session["return_url"]))
            session["return_url"] = None
        else:
            resp = make_response(render("success.html",
                                        social_access_token=social_access_token,
                                        aad_access_token=aad_access_token))
        return resp
    except Exception as ex:
        log.error(ex)
        return __login_failed(provider)


def __login_failed(provider):
    return redirect("/")

