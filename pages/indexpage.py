#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid
from datas import TransDate,calcProfit

class Host(object):
    def GET(self):
        if not database.session.get("uid",False):
            raise web.seeother('/wxauthstart')

        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"_id": 0})
        myproduct = []
        myproductls = []
        if "myproduct" in userinfo and userinfo["myproduct"]:
            myproductls = userinfo["myproduct"]
            del userinfo["myproduct"]
            myproduct = [key for key in myproductls.iterkeys()]

        allprofit=0
        products = []
        reminds=[]
        now=datetime.datetime.now()
        for one in database.lccp.find({"cpdjbm": {"$in": myproduct}}, {"_id": 0}).sort(
                [("yjkhzgnsyl", -1), ("cpyjzzrq", 1)]):
            one["profit"] = calcProfit(one,myproductls[one["cpdjbm"]])
            allprofit += one["profit"]
            dayremain=(now-one["cpyjzzrq"]).days
            if dayremain<14:
                if dayremain<0:
                    one["dayremain"]=0
                else:
                    one["dayremain"]=dayremain
                reminds.append(one)
            else:
                products.append(one)

        tpl=jinja2_env.get_template("index.html")
        return tpl.render(allprofit=allprofit,products=products,reminds=reminds)

class Guide(object):
    def GET(self):
        tpl = jinja2_env.get_template("guide.html")
        return tpl.render()

class ProfitDetail(object):
    def GET(self):
        params=web.input()
        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"myproduct.%s"%params.cpdjbm: 1})
        product=database.lccp.find_one({"cpdjbm": params.cpdjbm}, {"_id": 0})
        product["profit"] = calcProfit(product, userinfo["myproduct"][params.cpdjbm])
        now = datetime.datetime.now()
        dayremain = (now - product["cpyjzzrq"]).days

        if dayremain < 0:
            product["dayremain"] = 0
        else:
            product["dayremain"] = dayremain
        tpl = jinja2_env.get_template("profit-detail.html")
        return tpl.render(product=product,buystate=userinfo["myproduct"][params.cpdjbm],buytime=(now-userinfo["myproduct"][params.cpdjbm]["date"]).days)