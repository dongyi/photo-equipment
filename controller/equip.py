#coding=utf8
from common.base_httphandler import BaseHandler
from common.decorator import login_required
from tornado import database
"""
import sqlite3

conn = sqlite3.connect('new.db')
conn.text_factory = str
cur = conn.cursor()
"""
item_per_page = 20

convert_dict = {"5":"镜头类型","7":"发布日期","277":"厂家推荐价格","13":"焦距","19":"等效35mm画幅焦距","15":"最大光圈","16":"最小光圈","21":"视角","333":"镜头结构","12":"低/超低色散镜片","24":"光圈叶片","370":"最近对焦距离","25":"最大放大倍率","26":"驱动马达","27":"滤镜口径","540":"镜头卡口","754":"防抖","328":"颜色","368":"尺寸","31":"重量","329":"附件","492":"备注","496":"产品类型","334":"影像传感器","255":"影像传感器尺寸","279":"总像素","278":"有效像素","256":"影像处理器","402":"色彩滤镜","403":"低通滤镜","332":"最大解像度","314":"静态图像尺寸","510":"静态图像质量","539":"镜头卡口","401":"兼容镜头","344":"对焦系统类型","345":"对焦点","285":"对焦模式","286":"AF辅助灯","287":"手动对焦","289":"测光模式","351":"测光范围","290":"曝光模式","355":"快门类型","292":"快门速度","295":"曝光补偿","353":"自动曝光锁","352":"自动包围曝光","288":"ISO感光度","309":"白平衡","307":"自拍","305":"连拍","298":"闪光控制模式","483":"闪光同步模式","303":"专用闪光灯","335":"取景器","336":"取景范围","337":"取景放大倍率","404":"屈光度调节范围","342":"反光镜","341":"反光镜锁定","273":"LCD类型","273":"LCD类型","274":"LCD尺寸","275":"LCD像素","412":"Live View","414":"Live View 对焦模式","310":"存储卡","488":"数据接口","491":"视频接口","489":"支持打印协议","321":"电池","323":"电池寿命","330":"外接电源","490":"材质","328":"颜色","368":"尺寸","31":"重量","283":"支持语言","399":"画幅比","511":"色彩空间","312":"静态图像格式","340":"对焦屏","343":"景深预视","281":"视野率","522":"取景器信息","548":"配件端口","505":"测光系统","397":"工作温度","405":"自动对焦点选择","301":"闪光补偿","494":"用户自选功能","413":"Live View 显示","398":"工作湿度","315":"短片尺寸","313":"短片格式","297":"闪光灯类型"}



class EquipmentListHandler(BaseHandler):
    def get(self, page):
        page = int(page)
        start_id = (page-1)*item_per_page
        field_id = "id, item_name, item_type, item_brand, item_image"
        sql = "select %s from equipment limit %d, %d"%(field_id, start_id, item_per_page)
        res = self.db.query(sql)
        prev = max(1, page-1)
        next = min(62, page+1)
        cur_page = page
        self.render('equipment_list.html', res=res, prev=prev, next=next, cur_page=cur_page)

    def post():
        pass

class EquipmentHandler(BaseHandler):
    def get(self, action):
        if action == 'new':
            item = None
            return self.render('edit_equipment.html', item=item)
        elif action == 'edit':
            itemid = self.get_argument('itemid')
            sql = "select * from equipment where id=%s"%str(itemid)
            item = self.db.get(sql)
            return self.render('edit_equipment.html', item=item)
        else:
            equipmentid = action
            sql = "select id, item_name, item_brand, item_type, item_image from equipment where id=%d"%(int(equipmentid))
            res = self.db.get(sql)
            self.render('equipment.html', res=res)

    def post(self, action):
        f = lambda x:self.get_argument(x, '').strip()
        fields = map(lambda x:"attr_"+x, convert_dict.keys()) + 'item_name|item_brand|item_type|item_image'.split('|')
        if action == 'new':
            values = map(f, fields)
            sql = "INSERT INTO equipment(" + ",".join(fields) + ")VALUES('" + "','".join(values) + "')"
            self.db.execute(sql)
            return self.redirect('/')

        if action == 'edit':
            values = map(f, fields)
            sql = "DELETE FROM equipment where id=%d"%(f(id))
            self.db.execute(sql)
            sql = "INSERT INTO equipment(" + ",".join(fields) + ")VALUES('" + "','".join(values) + "')"
            self.db.execute(sql)
            return self.redirect('/')


class CategoryHandler(BaseHandler):
    def get(self, category):
        f = lambda x:self.get_argument(x, '').strip()
        if category == '':
            self.render('category.html')
        else:
            category = f('category')
            page = f('page')
            brand = f('brand')
            category = category.split('/')
            if len(category) > 1:
                category, page = category
            else:
                category, page = category[0], 1
            page = int(page)
            start_id = (page-1)*item_per_page
            condition = 'where %s'%'and'.join(['%s=%s'%(x, eval(x)) for x in ['brand', 'category']])
            sql = "select * from equipment where %s limit %d, %d"%(condition, start_id, item_per_page)
            print sql
            res = self.db.query(sql)
            prev = max(1, page-1)
            next = min(62, page+1)
            cur_page = page
            self.render('equipment_list.html', res=res, prev=prev, next=next, cur_page=cur_page)
