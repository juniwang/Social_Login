# -*- coding: utf-8 -*-
"""
Copyright (c) Microsoft Open Technologies (Shanghai) Co. Ltd.  All rights reserved.
 
The MIT License (MIT)
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import sys

sys.path.append("..")

from social_login.service.login_service import *
from social_login.user.oauth_login import *

from flask import Response, render_template, request, g, redirect, make_response, session, url_for, abort
from flask_login import login_user

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
def login():
    redirect_url = request.args.get("redirect_url", "")
    authorized_id = request.args.get("authorized_id", "")
    # ui_html is not provided by it but by javascript.

    #provider = request.args.get("provider")
    #prs = ["github", "qq", "gitcafe", "weibo", "live", "alauda"]

    #if provider is None:
    #    provider = safe_get_config("login.provider_enabled", prs)
    #else:
    #    provider = provider.split(',')

    service = LoginService()
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
    #openid = service.aad_manager.create_account("test_qq10" + safe_get_config("aad.default_domain", ""), "testqq", "testqq", "1234tEST")
    qq_login = QQLogin()
    social_access_token = qq_login.get_token(code)
    user_info = qq_login.get_info(social_access_token)
    openid = user_info["openid"]
    aad_token = service.get_aad_access_token(IDENTITY_PROVIDER.QQ, openid)

    #return render("success.html", aad_openid="111")
    return __login(LOGIN_PROVIDER.QQ, social_access_token, aad_token)
    #return render("error.html", message="qq fail to validate user.")

#@app.route('/weibo')
#def weibo_login():
#    return __login(LOGIN_PROVIDER.WEIBO)


#@app.route('/qq')
#def qq_login():
#    return __login(LOGIN_PROVIDER.QQ)

def __login(provider, social_token, aad_token):
    try:
        log.info("login successfully:")

        if session.get("return_url") is not None:
            resp = make_response(redirect(session["return_url"]))
            session["return_url"] = None
        else:
            resp = make_response(render("success.html", social_token=social_token, aad_token=aad_token))
        return resp
    except Exception as ex:
        log.error(ex)
        return __login_failed(provider)


def __login_failed(provider):
    return redirect("/")

