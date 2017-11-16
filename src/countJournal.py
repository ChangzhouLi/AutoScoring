# -*- coding:utf-8 -*-
import pymongo
import numpy as np
import os
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')
import time

##连接数据库
client = pymongo.MongoClient("222.200.166.138", 8815)

##输入账号密码
db_auth = client.admin
db_auth.authenticate("root", "sysu2016")

##连接数据库
db = client.newbimt

##连接表
collection = db.pubmed
##collection = db.cnki
##collection = db.wanfang
item = collection.find({'keyword_en': {'$ne': None}, \
                        'abstract_en': {'$ne': None}, \
                        'calssID': {'$ne': None}, \
                        'referenced.1': {'$exists': 1}}, \
                       {'keyword_en': 1, 'abstract_en': 1, 'referenced': 1, 'publishInfo': 1})

start = time.time()

count = {}
ind = 0
for row in item:
    # j_year = int(row['publishInfo']['year'])
    # if j_year == 1956:
    #     continue
    journal = str(row['publishInfo']['periodicalInfo']['name_en'])
    # print journal, ":", j_year
    if count.has_key(journal):
        count[journal] += 1
    else :
        count[journal] = 1

    ind += 1
    if(ind % 100000 == 0):
        print ind, 'cost time:', time.time() - start
    if(ind >= 200):
        break

print "total index:", ind, 'cost time:', time.time() - start


count = sorted(count.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

fout = open("journalList.txt", 'w')
for i, j in count:
    fout.writelines(i + '\t' + str(j) + '\n')

print "finished!!"
