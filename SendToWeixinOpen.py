#coding:utf8
import database
import weixin.basic
import urllib2
import json
import pycurl
import StringIO
import datetime
import base64
print "run at:",datetime.datetime.now()

def uploadThumbMedia(fname="./kejiji.jpg"):
    for i in xrange(10):
        try:
            c = pycurl.Curl()
            fp = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, fp.write)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.CONNECTTIMEOUT, 60)
            c.setopt(pycurl.TIMEOUT, 300)
            c.setopt(c.POST, 1)

            c.setopt(c.URL, "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=thumb"%weixin.basic.GetAccessToken())
            c.setopt(c.HTTPPOST, [("media", (c.FORM_FILE, fname))])
            c.perform()
            c.close()
            print(fp.getvalue())
            weixinimgdata=json.loads(fp.getvalue())
            thumb_media_id=weixinimgdata["thumb_media_id"]
            break
        except:
            pass
    return thumb_media_id
#default_thumb_media_id=GetDefaultImgid()

articles=[]
articles.append({
       "title": u"想发财就跟我来",
       "description": u"想发财就跟我来",
       "url": "http://www.baidu.com",
       "picurl": "http://www.weiyangx.com/wp-content/uploads/2014/02/%E7%A4%BE%E4%BC%9A%E5%80%9F%E8%B4%B7-%E4%BC%97%E7%AD%B9%E5%92%8CP2P%E8%B4%B7%E6%AC%BE.jpg"
})
datafile=open("templates/newprod.json")
productdata=json.load(datafile)
datafile.close()
for one in productdata:
    articles.append({
        "title": one["cpms"],
       "description": one["fxjgms"],
       "url": "http://news.wowfantasy.cn/host#productdetail?info="+base64.b64encode(json.dumps(one)),
       "picurl":"http://www.weiyangx.com/wp-content/uploads/2014/02/%E7%A4%BE%E4%BC%9A%E5%80%9F%E8%B4%B7-%E4%BC%97%E7%AD%B9%E5%92%8CP2P%E8%B4%B7%E6%AC%BE.jpg"
    })


if __name__ == '__main__':
    for i in xrange(10):
        try:
            c = pycurl.Curl()
            fp = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, fp.write)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.MAXREDIRS, 5)
            c.setopt(pycurl.CONNECTTIMEOUT, 60)
            c.setopt(pycurl.TIMEOUT, 300)
            c.setopt(c.POST, 1)

            c.setopt(c.URL, "https://api.weixin.qq.com/cgi-bin/message/mass/sendall?access_token=%s"%weixin.basic.GetAccessToken())
            c.setopt(pycurl.POSTFIELDS,  json.dumps({
                                       "filter":{
                                          "is_to_all":True
                                       },
                                       "news":{
                                                "articles":articles
                                                 },
                                       "msgtype":"news"
                                    },ensure_ascii=False).encode("utf-8"))
            c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json',])
            c.perform()
            c.close()
            print fp.getvalue()
            break
        except Exception,e:
            print e