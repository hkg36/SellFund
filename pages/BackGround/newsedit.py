#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid

class Editor(object):
    def GET(self):
        params=web.input()
        if params.has_key("delete") and params.delete:
            database.news.delete_one({"_id":objectid.ObjectId(params.delete)})
        articals=database.news.find({},{"content":0}).sort([("time",-1)]).limit(12)
        tpl = jinja2_env.get_template("background/newseditor.html")
        return tpl.render(articals=articals)

class EditorPage(object):
    def GET(self):
        param=web.input()
        art=None
        if param.has_key("id") and param.id:
            art=database.news.find_one({"_id":objectid.ObjectId(param.id)})
        tpl = jinja2_env.get_template("background/newseditorpage.html")
        return tpl.render(art=art)
    def POST(self):
        param=web.input(id="")
        artdata={
            "title": param.title,
            "brief": param.brief,
            "author": param.author,
            "content": param.content,
            "time":datetime.datetime.now(),
        }
        if len(param.id)==0:
            res=database.news.insert_one(artdata)
            return DefJsonEncoder.encode({"id":str(res.inserted_id),"res":0})
        else:
            database.news.update_one({"_id":objectid.ObjectId(param.id)},{"$set":artdata})
            return DefJsonEncoder.encode({"id":param.id,"res": 0})