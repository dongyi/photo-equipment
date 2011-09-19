#coding=utf8
from common.base_httphandler import BaseHandler
import sqlite3
conn = sqlite3.connect('new.db')
conn.text_factory = str
cur = conn.cursor()
item_per_page = 20


class EquipHandler(BaseHandler):
    def get(self, page):
        page = int(page)
        start_id = (page-1)*item_per_page
        sql = "select * from equipment limit %d, %d"%(start_id, item_per_page)
        cur.execute(sql)
        res = cur.fetchall()
        self.render('equipment.html', res=res)

    def post():
        pass
