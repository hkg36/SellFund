#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid

class Host(object):
    def GET(self):
        if not database.session.get("uid",False):
            raise web.seeother('/wxauthstart')
        tpl=jinja2_env.get_template("indexpage.html")
        return tpl.render()

class Guide(object):
    def GET(self):
        tpl = jinja2_env.get_template("guide.html")
        return tpl.render()