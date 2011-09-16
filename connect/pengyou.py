#coding=utf8

try:
    import ujson as json
except ImportError:
    import json

import common.lib_pengyou as pengyou
from common.base_httphandler import BaseHandler
from tornado.options import options

class MainHandler(BaseHandler):
    def get(self, action):
	if action == '':
	    openid, openkey = self.get_argument('openid'), self.get_argument('openkey')
	    self.set_cookie('openid', openid)
	    self.set_cookie('openkey', openkey)
	    self.render("templates/pengyou/index.html")

	if action == 'friendlist':
	    openid, openkey = self.get_cookie('openid'), self.get_cookie('openkey')
	    self.api = pengyou(options.pengyou_app_id, options.pengyou_app_key, options.pengyou_app_name, ('openapi.pengyou.qq.com',))
	    json_friend_list = self.api.getFriendList(openid,openkey,1,1)
	    friend_list = json.dumps(json_friend_list, ensure_ascii=False)
	    self.render("templates/friend_list.html", friend_list=friend_list)

	if action == 'get_info':
	    openid, openkey = self.get_cookie('openid'), self.get_cookie('openkey')
	    self.api = pengyou(options.pengyou_app_id, options.pengyou_app_key, options.pengyou_app_name, ('openapi.pengyou.qq.com',))
	    user_info = self.api.getUserinfo(openid, openkey)
	    self.render("templates/pengyou/user_info.html", user_info=user_info)


    def post(self):
        current_user = self.get_user_id()
        self.render("templates/pengyou/index.html", current_user=current_user)

