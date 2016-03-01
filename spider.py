#coding:utf8
import pycurl
import urllib
from StringIO import StringIO
import json
from bson import json_util
import pypinyin
import pymongo
import datetime
import re
import time

allcount=0
client = pymongo.MongoClient('mongodb://localhost:27017/')
fund = client.test
lccp=fund.lccp
lccp.create_index([("cpdjbm",pymongo.ASCENDING)],unique=True)

datalist=[]
for page in xrange(1,100000):
    while True:
        try:
            crl = pycurl.Curl()
            crl.setopt(pycurl.FOLLOWLOCATION, 0)
            crl.setopt(pycurl.MAXREDIRS, 5)
            crl.setopt(pycurl.USERAGENT,'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0')
            crl.setopt(pycurl.ENCODING,"gzip,deflate")
            crl.setopt(crl.POSTFIELDS,urllib.urlencode(
                    {"areacode":"110000",
                     "cpzt":"02,04",
                     "drawPageToolEnd":"5",
                     "pagenum":page}))
            crl.setopt(crl.POST, 1)
            crl.setopt(pycurl.CONNECTTIMEOUT, 6)
            crl.setopt(pycurl.TIMEOUT, 30)
            returnbody = StringIO()
            crl.setopt(pycurl.URL, "http://www.chinawealth.com.cn/lccpAllProJzyServlet.go")
            crl.setopt(crl.WRITEFUNCTION, returnbody.write)
            crl.setopt(pycurl.FOLLOWLOCATION, 1)
            crl.perform()
            rescode=crl.getinfo(pycurl.HTTP_CODE)
            if rescode==200:
                data=json.loads(returnbody.getvalue())
            allcount+=len(data["List"])
            break
        except:
            print "retry"
            time.sleep(20)
        finally:
            crl.close()
    for one in data["List"]:
        #cpztms=one["cpztms"]
        #cpdjbm=one["cpdjbm"]
        #del one["cpztms"]
        #del one["cpdjbm"]
        one["mjqsrq"]=datetime.datetime.strptime(one["mjqsrq"],"%Y/%m/%d")
        one["mjjsrq"]=datetime.datetime.strptime(one["mjjsrq"],"%Y/%m/%d")
        one["cpqsrq"]=datetime.datetime.strptime(one["cpqsrq"],"%Y/%m/%d")
        one["cpyjzzrq"]=datetime.datetime.strptime(one["cpyjzzrq"],"%Y/%m/%d")
        one["cpqx"]=int(one["cpqx"])
        one["qdxsje"]=int(one["qdxsje"])
        try:
            one["yjkhzgnsyl"]=float(one["yjkhzgnsyl"])
        except:
            pass
        try:
            one["yjkhzdnsyl"]=float(one["yjkhzdnsyl"])
        except:
            pass
        one["bank"]=re.sub(u"(股份|有限公司|（中国）)",u"",one["fxjgms"])
        datalist.append(one)
        #lccp.update_one({"cpdjbm":cpdjbm},{"$set":one,"$addToSet":{"cpztms":cpztms}},upsert=True)
    print allcount
    if data["Count"]<=allcount:
        break

lccp.remove({})
for one in datalist:
    cpztms=one["cpztms"]
    cpdjbm=one["cpdjbm"]
    del one["cpztms"]
    del one["cpdjbm"]
    lccp.update_one({"cpdjbm":cpdjbm},{"$set":one,"$addToSet":{"cpztms":cpztms}},upsert=True)
banks=[(one,"".join(pypinyin.lazy_pinyin(one))) for one in lccp.distinct("bank")]
banks=sorted(banks,key=lambda x:x[1])
banks=[one[0] for one in banks]
datafile=open("js/banklist.json","w")
json.dump(banks,datafile)
datafile.close()
"""
[ {
				"name" : "收益类型",
				"column" : "cpsylxms"
			}, {
				"name" : "运作模式",
				"column" : "cplxms"
			}, {
				"name" : "风险等级",
				"column" : "fxdjms"
			}, {
				"name" : "募集期",
				"column" : "mjqsrq",
				"to" : "mjjsrq"
			}, {
				"name" : "起售金额",
				"column" : "qdxsje",
				"unti" : "元"
			}, {
				"name" : "期限类型",
				"column" : "qxms"
			}, {
				"name" : "实际天数",
				"column" : "cpqx",
				"unti" : "天"
			}, {
				"name" : "存续期",
				"column" : "cpqsrq",
				"to" : "cpyjzzrq"
			}, {
				"name" : "发行机构",
				"column" : "fxjgms",
				"valtag" : "<span></span>",
				"clazz" : "noneImg"
			} ],
			special : [//特殊位置显示字段
			{
				"name" : "产品名称",
				"column" : "cpms"
			}, {
				"name" : "登记编码",
				"column" : "cpdjbm"
			}, {"column" : "cpid"
			}, {"name":"发行机构代码",
				"column":"fxjgdm"
			}],
			yield : [ {
				"name" : "预期最高收益率",
				"column" : "yjkhzgnsyl"
			}, {
				"name" : "预期最低收益率",
				"column" : "yjkhzdnsyl"
			} ],
			price : [ {
				"name" : "初始净值",
				"column" : "csjz"
			}, {
				"name" : "本期净值",
				"column" : "bqjz"
			}, {
				"name" : "截止到",
				"column" : "cpyjzzrq"
			} , {
				"name":"产品净值",
				"column":"cpjz"
			}]
		});
"""