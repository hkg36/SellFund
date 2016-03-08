#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid

class Login(object):
    def GET(self):
        openid="asdasde321321423"
        resdata={"openid":openid}
        database.users.update({"wx.openid":openid},{"$set":{"wx":resdata}},upsert=True)
        info=database.users.find_one({"wx.openid":openid},{"_id":1})
        database.session.uid=str(info["_id"])