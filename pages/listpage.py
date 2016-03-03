#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid
class ListPage(object):
    def GET(self):
        tpl=jinja2_env.get_template("favorites.html")
        return tpl.render()
    def POST(self):
        params=web.input(state=u"在售")
        findparam={"cpztms":params.state}
        try:
            userinfo=database.users.find_one({"_id":objectid.ObjectId(database.session.uid)},{"watchbanks":True})

            if userinfo and "watchbanks" in userinfo:
                findparam["bank"]={"$in":userinfo["watchbanks"]}
        except:
            pass
        alllist=database.lccp.find(findparam,{"_id":False})
        #alllist=database.lccp.find({},{"_id":False})
        if params.has_key("order") and params.order:
            alllist=alllist.sort(params.order)
        alllist=alllist.skip(int(params.page)*20).limit(20)
        datalist=[]
        for one in alllist:
            one["mjqsrq"]=one["mjqsrq"].strftime("%Y/%m/%d")
            one["mjjsrq"]=one["mjjsrq"].strftime("%Y/%m/%d")
            one["cpqsrq"]=one["cpqsrq"].strftime("%Y/%m/%d")
            one["cpyjzzrq"]=one["cpyjzzrq"].strftime("%Y/%m/%d")
            if isinstance(one["yjkhzgnsyl"],float):
                one["yjkhzgnsyl"]="{0:.2f}".format(one["yjkhzgnsyl"])
            if isinstance(one["yjkhzdnsyl"],float):
                one["yjkhzdnsyl"]="{0:.2f}".format(one["yjkhzdnsyl"])
            datalist.append(one)
        data={"list":datalist}
        return json.dumps(data,default=json_util,separators=(',', ':'))

class BankSelector(object):
    def GET(self):
        tpl=jinja2_env.get_template("bankSel.html")
        userinfo=database.users.find_one({"_id":objectid.ObjectId(database.session.uid)},{"watchbanks":True})
        selectedbank=[]
        if userinfo and "watchbanks" in userinfo:
            selectedbank=userinfo["watchbanks"]
        return tpl.render(selectedbank=json.dumps(selectedbank))
    def POST(self):
        data=web.data()
        banklist=json.loads(data)
        database.users.update({"_id":objectid.ObjectId(database.session.uid)},{"$set":{"watchbanks":banklist}})
        resdata={}
        return json.dumps(resdata)