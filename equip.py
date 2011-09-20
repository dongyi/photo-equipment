#coding=utf8
from common.base_httphandler import BaseHandler
import sqlite3
conn = sqlite3.connect('new.db')
conn.text_factory = str
cur = conn.cursor()
item_per_page = 20

convert_dict = {"5":"镜头类型","7":"发布日期","277":"厂家推荐价格","13":"焦距","19":"等效35mm画幅焦距","15":"最大光圈","16":"最小光圈","21":"视角","333":"镜头结构","12":"低/超低色散镜片","24":"光圈叶片","370":"最近对焦距离","25":"最大放大倍率","26":"驱动马达","27":"滤镜口径","540":"镜头卡口","754":"防抖","328":"颜色","368":"尺寸","31":"重量","329":"附件","492":"备注","496":"产品类型","334":"影像传感器","255":"影像传感器尺寸","279":"总像素","278":"有效像素","256":"影像处理器","402":"色彩滤镜","403":"低通滤镜","332":"最大解像度","314":"静态图像尺寸","510":"静态图像质量","539":"镜头卡口","401":"兼容镜头","344":"对焦系统类型","345":"对焦点","285":"对焦模式","286":"AF辅助灯","287":"手动对焦","289":"测光模式","351":"测光范围","290":"曝光模式","355":"快门类型","292":"快门速度","295":"曝光补偿","353":"自动曝光锁","352":"自动包围曝光","288":"ISO感光度","309":"白平衡","307":"自拍","305":"连拍","298":"闪光控制模式","483":"闪光同步模式","303":"专用闪光灯","335":"取景器","336":"取景范围","337":"取景放大倍率","404":"屈光度调节范围","342":"反光镜","341":"反光镜锁定","273":"LCD类型","273":"LCD类型","274":"LCD尺寸","275":"LCD像素","412":"Live View","414":"Live View 对焦模式","310":"存储卡","488":"数据接口","491":"视频接口","489":"支持打印协议","321":"电池","323":"电池寿命","330":"外接电源","490":"材质","328":"颜色","368":"尺寸","31":"重量","283":"支持语言","399":"画幅比","511":"色彩空间","312":"静态图像格式","340":"对焦屏","343":"景深预视","281":"视野率","522":"取景器信息","548":"配件端口","505":"测光系统","397":"工作温度","405":"自动对焦点选择","301":"闪光补偿","494":"用户自选功能","413":"Live View 显示","398":"工作湿度","315":"短片尺寸","313":"短片格式","297":"闪光灯类型"}


class EquipmentListHandler(BaseHandler):
    def get(self, page):
        page = int(page)
        start_id = (page-1)*item_per_page
        sql = "select * from equipment limit %d, %d"%(start_id, item_per_page)
        cur.execute(sql)
        res = cur.fetchall()
        prev = max(1, page-1)
        next = min(62, page+1)
        cur_page = page
        self.render('equipment_list.html', res=res, prev=prev, next=next, cur_page=cur_page)

    def post():
        pass

class EquipmentHandler(BaseHandler):
    def get(self, equipmentid):
        sql = "select * from equipment where id=%d"%(int(equipmentid))
        cur.execute(sql)
        res = cur.fetchall()
        self.render('equipment.html', res=res)

class CategoryHandler(BaseHandler):
    def get(self, category):
        if category == '':
            self.render('category.html')
        else:
            category = category.split('/')
            if len(category) > 1:
                category, page = category
            else:
                category, page = category[0], 1
            page = int(page)
            start_id = (page-1)*item_per_page
            sql = "select * from equipment where item_type='%s' limit %d, %d"%(category, start_id, item_per_page)
            cur.execute(sql)
            res = cur.fetchall()
            prev = max(1, page-1)
            next = min(62, page+1)
            cur_page = page
            self.render('equipment_list.html', res=res, prev=prev, next=next, cur_page=cur_page)
