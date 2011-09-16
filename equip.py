from base_httphandler import BaseHandler
import sqlite3
conn = sqlite3.connect('equipment.db')
cur = conn.cur
item_per_page = 20


class EquipHandler(BaseHandler):
    def get(self, page):
        page = int(page)
        min_id, max_id = page*item_per_page, (page+1)*item_per_page
        sql = "select * from equipment where  %d < id < %d"%(min_id, max_id)
        cur.execute(sql)
        res = cur.fetchall()
        self.render('equipment.html', res)

    def post():
        pass
