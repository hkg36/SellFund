#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid

class Search(object):
    def POST(self):
        params=web.input(page=0)
        findparam={"cpms" : {'$regex' : ".*%s.*"%params.text}}
        alllist=database.lccp.find(findparam,{"_id":False})
        if params.has_key("order") and params.order:
            if params.order[0]=="-":
                alllist=alllist.sort(((params.order[1:],-1),))
            else:
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
            one["buy_value"]=myproductls[one["cpdjbm"]]
            one["mjqsrq"]=one["mjqsrq"].strftime("%Y/%m/%d")
            one["mjjsrq"]=one["mjjsrq"].strftime("%Y/%m/%d")
            one["cpqsrq"]=one["cpqsrq"].strftime("%Y/%m/%d")
            one["cpyjzzrq"]=one["cpyjzzrq"].strftime("%Y/%m/%d")
            if isinstance(one["yjkhzgnsyl"],float):
                one["yjkhzgnsyl"]="{0:.2f}".format(one["yjkhzgnsyl"])
            if isinstance(one["yjkhzdnsyl"],float):
                one["yjkhzdnsyl"]="{0:.2f}".format(one["yjkhzdnsyl"])
            products.append(one)

        return DefJsonEncoder.encode({"list":products})