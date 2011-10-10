#coding=utf8

import os
import urllib

import MySQLdb
conn = MySQLdb.connect(user='root', passwd='root', db='photo')
cur = conn.cursor()
item_per_page = 20


sql = "select item_image from equipment where id>1132"
cur.execute(sql)
res = cur.fetchall()

for i in res:
    url = "http://www2.xitek.com/production/" + i[0]
    if i[0] != "no image":
        dow_dir = "/home/dongyi/code/photo-equipment/static/uploads/pictures/" + i[0].split('/')[-2]
        if not os.path.exists(dow_dir): os.mkdir(dow_dir)
        down_path = dow_dir + "/" + i[0].split('/')[-1]
        data = urllib.urlopen(url).read()
        f = file(down_path,"wb")
        f.write(data)
        f.close()
