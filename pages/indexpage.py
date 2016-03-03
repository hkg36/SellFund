#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid

class DemoPage(object):
    def GET(self):
        tpl=jinja2_env.get_template("indexpage.html")
        return tpl.render()