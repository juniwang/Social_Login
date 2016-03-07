# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Api

from util import *
from log import log


# initialize flask and flask restful
app = Flask(__name__)

# init restful API
api = Api(app)

from views import *