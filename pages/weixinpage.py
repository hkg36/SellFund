import web
from pages import *
import weixin.basic
import random,string
import time
import hashlib
import json
import urllib
import urllib2
import database
import pymongo

database.users.create_index([("wx.openid",pymongo.ASCENDING)],unique=True,sparse=True)
class WeiXinTest(object):
    def GET(self):
        tpl=jinja2_env.get_template("weixinhost.html")
        return tpl.render()

class WeiXinSign(object):
    def POST(self):
        param=web.input()
        pos=param.url.find("#")
        if pos>0:
            param.url=param.url[:pos]
        jsapi_ticket=weixin.basic.GetJSApiTicket()
        noncestr=''.join(random.choice(string.ascii_letters+ string.digits) for _ in range(10))
        timestamp=int(time.time())
        checkstr="jsapi_ticket=%s&noncestr=%s&timestamp=%d&url=%s"%(jsapi_ticket,noncestr,timestamp,param.url)
        signature=hashlib.sha1(checkstr).hexdigest()
        return json.dumps({'appId':weixin.basic.APPID,
            'timestamp': timestamp,
            'nonceStr': noncestr,
            'signature': signature,
                           "url":param.url })

class WeiXinStartAuth(object):
    def GET(self):
        param=web.input(state='')
        urlparam=urllib.urlencode((
            ("appid",weixin.basic.APPID),
            ("redirect_uri","http://news.wowfantasy.cn/weixinindex"),
            ("response_type","code"),
            ("scope","snsapi_userinfo"),
            ("state",param.state),
        ))
        web.seeother("https://open.weixin.qq.com/connect/oauth2/authorize?"+urlparam+"#wechat_redirect")

class WeiXinFinishAuth(object):
    def GET(self):
        param=web.input(code=None,state=None)
        if param.code:
            res=urllib2.urlopen("https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code"%
                            (weixin.basic.APPID,weixin.basic.APPSECRET,param.code))
            resdata=json.loads(res.read())
            openid=resdata["openid"]
            access_token=resdata["access_token"]
            resdata["expires"]=time.time()+resdata["expires_in"]
            database.users.update({"wx.openid":openid},{"$set":{"wx":resdata}},upsert=True)

            info=database.users.find_one({"wx.openid":openid},{"_id":1})
            database.session.uid=str(info["_id"])

            res=urllib2.urlopen("https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN"%(access_token,openid))
            resdata=json.loads(res.read())
            del resdata["openid"]
            if "unionid" in resdata:
                del resdata["unionid"]
            database.users.update({"wx.openid":openid},{"$set":{"wxinfo":resdata}})

            if param.state:
                web.seeother("/"+param.state)
            else:
                web.seeother("/host")