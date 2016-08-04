#coding:utf8
import html5lib
import urllib2
import sqlite3
from pyquery import PyQuery as pq
htmlparser2 = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("lxml"),namespaceHTMLElements=False)
database_temp=sqlite3.connect("/tmp/spider.db")
try:
    database_temp.execute("create table urlspider(url varchar(1024) PRIMARY KEY,bank varchar(100),area varchar(100),city varchar(100),done int default 0)")
except Exception,e:
    print e
try:
    database_temp.execute("create table halllist(hall varchar(100) PRIMARY KEY,addr VARCHAR(100),phone varchar(100),bank varchar(100),area varchar(100),city varchar(100))")
except Exception,e:
    print e

def FetchTable(url):
    req = urllib2.Request("http://www.pplive114.com"+url)
    respons = urllib2.urlopen(req)
    data = respons.read()
    doc = htmlparser2.parse(data)
    root = pq(doc.getroot())
    trs=root("#main-h-1 table tr")
    datalist=[]
    for tr in trs[1:]:
        tr=pq(tr)
        tds=tr.find("td")
        hall=pq(tds[0]).text().strip()
        addr=pq(tds[1]).text().strip()
        phone = pq(tds[2]).text().strip()
        datalist.append((hall,addr,phone))
    return datalist

city=u"北京"
for i in xrange(1,33):
    req=urllib2.Request("http://www.pplive114.com/Bank/%d/beijing/"%i)
    respons=urllib2.urlopen(req)
    data=respons.read()
    doc=htmlparser2.parse(data)
    root=pq(doc.getroot())
    bank=root("#position-h-1 .class3").attr("title")
    bk=root("#Bank1")
    a_s=pq(bk[0]).find("a")
    cur=database_temp.cursor()
    for a in a_s:
        url=a.attrib["href"]
        area=a.attrib["title"]
        cur.execute("insert or replace into urlspider(url,bank,area,city) values(?,?,?,?)",(url,bank,area,city))
    cur.close()
    database_temp.commit()

while True:
    cur=database_temp.cursor()
    cur.execute("select url,bank,area,city from urlspider where done!=1 limit 5")
    procs=cur.fetchall()
    if len(procs)==0:
        break
    for line in procs:
        halls=FetchTable(line[0])
        for hall in halls:
            cur.execute("insert or replace into halllist(hall,addr,phone,bank,area,city) values(?,?,?,?,?,?)",
                        (hall[0],hall[1],hall[2],line[1],line[2],line[3]))
        cur.execute("update urlspider set done=1 where url=?",(line[0],))
        print line[0],"done"
    cur.close()
    database_temp.commit()
database_temp.close()
