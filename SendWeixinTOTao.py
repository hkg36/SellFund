import SendToWeixinOpen
import json
import urllib2
import weixin.basic
import pycurl
import StringIO

c = pycurl.Curl()
fp = StringIO.StringIO()
c.setopt(pycurl.WRITEFUNCTION, fp.write)
c.setopt(pycurl.FOLLOWLOCATION, 1)
c.setopt(pycurl.MAXREDIRS, 5)
c.setopt(pycurl.CONNECTTIMEOUT, 60)
c.setopt(pycurl.TIMEOUT, 300)
c.setopt(c.POST, 1)

c.setopt(c.URL, "https://api.weixin.qq.com/cgi-bin/message/mass/preview?access_token=%s"%weixin.basic.GetAccessToken())
c.setopt(pycurl.POSTFIELDS,  json.dumps({
                           "towxname":"shutup_man",
                           "news":{
                                    "articles":SendToWeixinOpen.articles
                                     },
                           "msgtype":"news"
                        },ensure_ascii=False).encode("utf-8"))
c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json',])
c.perform()
c.close()

print fp.getvalue()
