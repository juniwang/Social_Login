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

from login_agent import *
from login_agent.service.login_service import *
from flask import Response, render_template, request, g, redirect, make_response, session, url_for, abort

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
    if service.validate_request(redirect_url, authorized_id):
        return render("login.html")
    return render("error.html", message="fail to validate developer.")

# js config
@app.route('/config.js')
def js_config():
    resp = Response(response="var CONFIG=%s" % json.dumps(get_config("javascript")),
                    status=200,
                    mimetype="application/javascript")
    return resp

@app.route("/qq")
def qq_login():
    access_token = request.args.get("code", "")

    service = LoginService()
    #if service.validate_request(redirect_url, authorized_id):
    return render("success.html")
    #return render("error.html", message="qq fail to validate user.")





#def init_routes():
