#coding=utf8
import sqlite3
import os
import urllib
conn = sqlite3.connect('new.db')
conn.text_factory = str
cur = conn.cursor()
item_per_page = 20


sql = "select item_image from equipment"
cur.execute(sql)
res = cur.fetchall()

for i in res:
    url = "http://www2.xitek.com/production/" + i[0]
    if i[0] != "no image":
        dow_dir = "uploads/pictures/" + i[0].split('/')[-2]
        if not os.path.exists(dow_dir): os.mkdir(dow_dir)
        down_path = dow_dir + "/" + i[0].split('/')[-1]
        data = urllib.urlopen(url).read()
        f = file(down_path,"wb")
        f.write(data)
        f.close()
