# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from datetime import timedelta

from util import *
from log import log


# initialize flask and flask restful
app = Flask(__name__)

# init restful API
api = Api(app)

def init_app():
    """Initialize the application.

    Works including :
        - register restful API routes
    """

    #from views import init_routes
    #init_routes()

init_app()

from views import *