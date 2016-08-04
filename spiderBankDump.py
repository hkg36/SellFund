#coding:utf-8
import database
import sqlite3
database.bankbranch.create_index([("hall",1),],unique=True)
database_temp=sqlite3.connect("/tmp/spider.db")
cur=database_temp.cursor()
cur.execute("select * from halllist")
while True:
    row=cur.fetchone()
    if row is None:
        break
    database.bankbranch.update_one({"hall":row[0]},
                                   {"$set":
                                        {"addr":row[1],
                                         "phone":row[2],
                                         "bank":row[3],
                                         "area":row[4],
                                         "city":row[5]}},upsert=True)