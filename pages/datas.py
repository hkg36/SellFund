#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid

def TransDate(one):
    one["mjqsrq"]=one["mjqsrq"].strftime("%Y/%m/%d")
    one["mjjsrq"]=one["mjjsrq"].strftime("%Y/%m/%d")
    one["cpqsrq"]=one["cpqsrq"].strftime("%Y/%m/%d")
    one["cpyjzzrq"]=one["cpyjzzrq"].strftime("%Y/%m/%d")
    if isinstance(one["yjkhzgnsyl"],float):
        one["yjkhzgnsyl"]="{0:.2f}".format(one["yjkhzgnsyl"])
    if isinstance(one["yjkhzdnsyl"],float):
        one["yjkhzdnsyl"]="{0:.2f}".format(one["yjkhzdnsyl"])
class Search(object):
    def POST(self):
        params=web.input(page=0)
        findparam={}
        if params.has_key("text") and params.text:
            findparam["cpms"] = {'$regex' : ".*%s.*"%params.text}
        alllist=database.lccp.find(findparam,{"_id":False})
        if params.has_key("order") and params.order:
            if params.order[0]=="-":
                alllist=alllist.sort(((params.order[1:],-1),))
            else:
                alllist=alllist.sort(params.order)
        alllist=alllist.skip(int(params.page)*20).limit(20)
        datalist=[]
        for one in alllist:
            TransDate(one)
            datalist.append(one)
        data={"list":datalist}
        return json.dumps(data,default=json_util,separators=(',', ':'))

class WatchBank(object):
    def GET(self):
        selectedbank=[]
        try:
            userinfo=database.users.find_one({"_id":objectid.ObjectId(database.session.uid)},{"watchbanks":True})
            if userinfo and "watchbanks" in userinfo:
                selectedbank=userinfo["watchbanks"]
        except:
            pass
        return json.dumps(selectedbank)
    def POST(self):
        data=web.data()
        banklist=json.loads(data)
        database.users.update({"_id":objectid.ObjectId(database.session.uid)},{"$set":{"watchbanks":banklist}})
        resdata={}
        return json.dumps(resdata)

class RecordBuy(object):
    def POST(self):
        param=web.input()
        database.users.update({"_id":objectid.ObjectId(database.session.uid)},
                              {"$set":{"myproduct."+param.cpdjbm:{"value":float(param.value),"date":datetime.datetime.strptime(param.date,"%Y-%m-%d")}}})
        return json.dumps({})

class DoWatch(object):
    def GET(self):
        param=web.input()
        if "remove" in param:
            database.users.update({"_id":objectid.ObjectId(database.session.uid)},{"$pull":{"watchproduct":param.cpdjbm}})
        else:
            database.users.update({"_id":objectid.ObjectId(database.session.uid)},{"$addToSet":{"watchproduct":param.cpdjbm}})
        return json.dumps({})

class MyInfo(object):
    def GET(self):
        userinfo=database.users.find_one({"_id":objectid.ObjectId(database.session.uid)},{"_id":0})
        myproduct=[]
        myproductls=[]
        if "myproduct" in userinfo and userinfo["myproduct"]:
            myproductls=userinfo["myproduct"]
            del userinfo["myproduct"]
            myproduct=[key for key in myproductls.iterkeys()]

        products=[]
        for one in database.lccp.find({"cpdjbm":{"$in":myproduct}},{"_id":0}):
            TransDate(one)
            one["buy_value"]=myproductls[one["cpdjbm"]]
            products.append(one)

        return DefJsonEncoder.encode({"list":products})

class WatchProduct(object):
    def GET(self):
        products=[]
        userinfo=database.users.find_one({"_id":objectid.ObjectId(database.session.uid)},{"watchproduct":1,"myproduct":1})
        if "watchproduct" in userinfo:
            watchproduct=userinfo["watchproduct"]

            for one in database.lccp.find({"cpdjbm":{"$in":watchproduct}},{"_id":0}):
                TransDate(one)
                products.append(one)
        return DefJsonEncoder.encode({"list":products})

class NewsList(object):
    def GET(self):
        news=[]
        for one in database.news.find({},{"content":0}).sort([("time",-1)]).limit(12):
            one["_id"]=str(one["_id"])
            one["time"]=one["time"].strftime("%Y-%m-%d %H-%M-%S")
            news.append(one)
        return DefJsonEncoder.encode({"news":news})
class OneNews(object):
    def GET(self):
        params=web.input()
        art=database.news.find_one({"_id":objectid.ObjectId(params.id)},{"brief":0})
        art["_id"]=str(art["_id"])
        art["time"] = art["time"].strftime("%Y-%m-%d %H:%M:%S")
        return DefJsonEncoder.encode(art)