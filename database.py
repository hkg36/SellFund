import memcache
import pymongo
memclient=memcache.Client(['127.0.0.1:11211'])
session=None

client = pymongo.MongoClient('mongodb://localhost:27017/')
fund = client.test
lccp=fund.lccp
users=fund.users