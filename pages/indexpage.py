#coding:utf8
from pages import *
import web
import json
import database
import datetime
from bson import json_util,objectid
from datas import TransDate,calcProfit
import dateutil

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
        finish = []
        now=datetime.datetime.now()
        for one in database.lccp.find({"cpdjbm": {"$in": myproduct}}, {"_id": 0}).sort(
                [("yjkhzgnsyl", -1), ("cpyjzzrq", 1)]):
            one["profit"] = calcProfit(one,myproductls[one["cpdjbm"]])
            allprofit += one["profit"]
            dayremain=(one["cpyjzzrq"]-now).days
            if dayremain<=0:
                finish.append(one)
            else:
                products.append(one)

        tpl=jinja2_env.get_template("index.html")
        return tpl.render(allprofit=allprofit,products=products,finish=finish)

class Remind(object):
    def GET(self):
        if not database.session.get("uid", False):
            raise web.seeother('/wxauthstart')

        params = web.input()
        if params.has_key("rmday"):
            database.users.update_one({"_id": objectid.ObjectId(database.session.uid)},{"$set":{'rmday':int(params.rmday)}})
        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"_id": 0})
        myproduct = []
        myproductls = []
        if "myproduct" in userinfo and userinfo["myproduct"]:
            myproductls = userinfo["myproduct"]
            del userinfo["myproduct"]
            myproduct = [key for key in myproductls.iterkeys()]

        if 'rmday' in userinfo:
            days=userinfo['rmday']
        else:
            days=7

        allprofit = 0
        reminds = []
        finish=[]
        now = datetime.datetime.now()
        for one in database.lccp.find({"cpdjbm": {"$in": myproduct}}, {"_id": 0}).sort(
                [("yjkhzgnsyl", -1), ("cpyjzzrq", 1)]):
            one["profit"] = calcProfit(one, myproductls[one["cpdjbm"]])
            allprofit += one["profit"]
            dayremain = (one["cpyjzzrq"] - now).days
            if dayremain<days:
                if dayremain<0:
                    finish.append(one)
                else:
                    one["dayremain"]=dayremain
                    reminds.append(one)

        tpl = jinja2_env.get_template("my-remind.html")
        return tpl.render(allprofit=allprofit, reminds=reminds,days=days,finish=finish)

class RegProduct(object):
    def GET(self):
        tpl = jinja2_env.get_template("addrecord.html")
        return tpl.render()
class Guide(object):
    def GET(self):
        params = web.input(step=1)
        step=int(params.step)
        if step==1:
            tpl = jinja2_env.get_template("welcome1.html")
        if step == 2:
            tpl = jinja2_env.get_template("welcome2.html")
        if step == 3:
            tpl = jinja2_env.get_template("welcome3.html")
        return tpl.render()
    def POST(self):
        params = web.input()
        cpdjbm=params.cpdjbm
        value=params.value
        time=params.time
        rec=database.lccp.find_one({"cpdjbm":cpdjbm},{"cpms":True})
        if rec==None:
            return u"产品不存在"
        database.users.update({"_id": objectid.ObjectId(database.session.uid)},
                              {"$set": {"myproduct." + cpdjbm: {"value": float(value),
                                                                      "date": datetime.datetime.strptime(time,
                                                                                                         "%Y-%m-%d")}}})
        return u"成功录入:"+rec["cpms"]

class ProfitDetail(object):
    def GET(self):
        params=web.input()
        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"myproduct.%s"%params.cpdjbm: 1})
        product=database.lccp.find_one({"cpdjbm": params.cpdjbm}, {"_id": 0})
        product["profit"] = calcProfit(product, userinfo["myproduct"][params.cpdjbm])
        now = datetime.datetime.now()
        dayremain = (product["cpyjzzrq"] -now ).days

        if dayremain < 0:
            product["dayremain"] = 0
        else:
            product["dayremain"] = dayremain
        tpl = jinja2_env.get_template("profit-detail.html")
        if "date" in userinfo["myproduct"][params.cpdjbm]:
            buytime=(now-userinfo["myproduct"][params.cpdjbm]["date"]).days
        else:
            buytime=0
        return tpl.render(product=product,buystate=userinfo["myproduct"][params.cpdjbm],buytime=buytime)
    def POST(self):
        params = web.input()
        if params.act=="del":
            database.users.update_one({"_id": objectid.ObjectId(database.session.uid)},
                                      {"$unset":{"myproduct.%s" % params.cpdjbm: 1}})

class MySelect(object):
    def __init__(self):
        self.tplname="select.html"
    def GET(self):
        params=web.input(search=None,order="-yjkhzgnsyl",page=0)
        findparam = {}
        if params.search:
            findparam["cpms"] = {'$regex': ".*%s.*" % params.search}
            findparam={"$and":[{"mjjsrq": {"$gt": datetime.datetime.now()}},findparam]}
        else:
            findparam = {"mjjsrq": {"$gt": datetime.datetime.now()}}
        self.BuildFindParam(findparam)

        alllist = database.lccp.find(findparam, {"_id": False})
        if params.order:
            if params.order[0] == "-":
                alllist = alllist.sort(((params.order[1:], -1),))
            else:
                alllist = alllist.sort(params.order)
        alllist = alllist.skip(int(params.page) * 200).limit(200)
        tpl = jinja2_env.get_template(self.tplname)
        return tpl.render(alllist=alllist,order=params.order)
    def BuildFindParam(self,findparam):
        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"watchbanks": True})
        if userinfo and "watchbanks" in userinfo:
            selectedbank = userinfo["watchbanks"]
            if selectedbank:
                findparam["bank"] = {"$in": selectedbank}
class MySelectOtherBank(MySelect):
    def __init__(self):
        super(MySelectOtherBank,self).__init__()
        self.tplname="waidiyinhang.html"
    def BuildFindParam(self,findparam):
        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"attentionbanks": True})
        if userinfo and "attentionbanks" in userinfo:
            selectedbank = userinfo["attentionbanks"]
            if selectedbank:
                findparam["bank"] = {"$in": selectedbank}
class ProductDetail(object):
    def GET(self):
        param=web.input(hidereserve=0)
        product=database.lccp.find_one({"cpdjbm": param.cpdjbm}, {"_id": 0})
        tpl = jinja2_env.get_template("product-detail.html")
        return tpl.render(product=product,hidereserve=int(param.hidereserve))

class MyBank(object):
    def GET(self):
        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"watchbanks": True})
        selectedbank=[]
        if userinfo and "watchbanks" in userinfo:
            selectedbank = userinfo["watchbanks"]
        tpl = jinja2_env.get_template("my-bank.html")
        return tpl.render(selectedbank=json.dumps(selectedbank))
    def POST(self):
        params=web.input()
        cb=params.banks
        cb=json.loads(cb)
        database.users.update_one({"_id": objectid.ObjectId(database.session.uid)},{"$set":{"watchbanks":cb}})

class MyAttention(object):
    def GET(self):
        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"attentionbanks": True})
        selectedbank = []
        if userinfo and "attentionbanks" in userinfo:
            selectedbank = userinfo["attentionbanks"]
        tpl = jinja2_env.get_template("my-attention.html")
        return tpl.render(selectedbank=json.dumps(selectedbank))
    def POST(self):
        params=web.input()
        cb=params.banks
        cb = json.loads(cb)
        database.users.update_one({"_id": objectid.ObjectId(database.session.uid)}, {"$set": {"attentionbanks": cb}})

class MyReserve(object):
    def GET(self):
        userinfo = database.users.find_one({"_id": objectid.ObjectId(database.session.uid)}, {"reserve": 1})
        products=[]
        if userinfo and "reserve" in userinfo:
            reserve=userinfo["reserve"]
            products=database.lccp.find({"$and": [{"cpdjbm": {"$in": reserve}},
                                         {"mjjsrq": {"$gt": datetime.datetime.now() + datetime.timedelta(days=0)}}]},
                               {"_id": 0}).sort([("yjkhzgnsyl", -1), ("cpyjzzrq", 1)])
        tpl = jinja2_env.get_template("my-reserve.html")
        return tpl.render(products=products)
    def POST(self):
        params=web.input()
        if params.cmd=='add':
            res=database.users.update_one({"_id": objectid.ObjectId(database.session.uid)},
                                  {"$addToSet": {"reserve": params.cpdjbm}})
            print res

class RegBuy(object):
    def GET(self):
        params = web.input()
        product=database.lccp.find_one({"cpdjbm": params.cpdjbm})
        tpl = jinja2_env.get_template("buy.html")
        return tpl.render(product=product)
    def POST(self):
        param = web.input()
        database.users.update({"_id": objectid.ObjectId(database.session.uid)},
                              {"$set": {"myproduct." + param.cpdjbm: {"value": float(param.value),
                                                                      "date": datetime.datetime.strptime(param.date,
                                                                                                         "%Y-%m-%d")}}})
        return json.dumps({})

class RoundBank(object):
    def GET(self):
        params = web.input()
        #list=database.bankbranch.find({"bank":params.bank})
        tpl = jinja2_env.get_template("round-bank.html")
        return tpl.render(bank=params.bank)#,list=list)

class Recommend(object):
    def GET(self):
        params = web.input()
        searchparam = {}
        after = None
        if params.has_key("after"):
            after = dateutil.parser.parse(params.after)
            searchparam["mjjsrq"] = {"$gt": after, "$lt": after + datetime.timedelta(days=14)}
        products=database.lccp.find(searchparam, {"_id": 0}).sort("yjkhzgnsyl", -1).limit(30)
        tpl = jinja2_env.get_template("recommend.html")
        return tpl.render(products=products)

class Revise(object):
    def GET(self):
        params = web.input()
        cpdjbm=params.cpdjbm
        tpl = jinja2_env.get_template("revise.html")
        return tpl.render(cpdjbm=cpdjbm)
    def POST(self):
        param = web.input()
        database.users.update({"_id": objectid.ObjectId(database.session.uid)},
                              {"$set": {"myproduct." + param.cpdjbm: {"value": float(param.value),
                                                                      "profit":float(param.profit)}}})
