#coding:utf-8
import web
import database

class MemCacheStore(web.session.Store):
    mc = None
    def __init__(self):
        self.mc = database.memclient
    def __contains__(self, key):
        return self.mc.get(key) != None
    def __getitem__(self, key):
        return self.mc.get(key)
    def __setitem__(self, key, value):
        self.mc.set(key, value, time = web.config.session_parameters["timeout"])
    def __delitem__(self, key):
        self.mc.delete(key)
    def cleanup(self, timeout):
        pass # Not needed as we assigned the timeout to memcache
class StaticFile:
    def GET(self, media, file):
        try:
            f = open("{0}/{1}".format(media,file), 'r')
            return f.read()
        except:
            return '' # you can send an 404 error here if you want

import pages.listpage
import pages.weixinpage
import pages.indexpage
import pages.datas
web.config.debug = False
path_list=['/list', pages.listpage.ListPage,
           '/demo',pages.indexpage.DemoPage,
           '/banksel',pages.listpage.BankSelector,
           '/weixin', pages.weixinpage.WeiXinTest,
           '/wxsign',pages.weixinpage.WeiXinSign,
           '/weixinindex',pages.weixinpage.WeiXinFinishAuth,
           '/wxauthstart',pages.weixinpage.WeiXinStartAuth,
           '/datas/search',pages.datas.Search]
path_list.extend(("/(js|css|images|style)/(.*)",StaticFile))
webapp=web.application(path_list, locals())
database.session = web.session.Session(webapp, MemCacheStore(), initializer={'count': 0})
del path_list
application = webapp.wsgifunc()
