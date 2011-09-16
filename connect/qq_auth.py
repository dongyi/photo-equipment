#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pengyou import pengyou
from common.base_httphandler import BaseHandler


class QQLoginHandler(BaseHandler):
    def current_user(self):
        openid, openkey = self.get_cookie('openid'), self.get_cookie('openkey')
        self.api = pengyou(options.pengyou_app_id, options.pengyou_app_key, options.pengyou_app_name, ('openapi.pengyou.qq.com',))
        user_info = self.api.getUserinfo(openid, openkey)
        self.render("qq/user_info.html", user_info=user_info)

    def get(self):
        pass

class QQLogoutHandler(BaseHandler):
    def get(self):
        pass

