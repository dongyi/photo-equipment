#coding=utf8

import uuid

from common.base_httphandler import BaseHandler

class temp:
    pass

class TempLoginHandler(BaseHandler):
    def get(self):
	self.session['platform'] = 'temp'
	self.session['username'] = str(uuid.uuid4().int)
	self.session['oauth_access_token'] = uuid.uuid4().int
	me = temp()
	me.id = uuid.uuid4().int
	me.name = str(uuid.uuid4().int)
	me.url = 'http://www.google.com'
	me.profile_image_url = 'http://img3.douban.com/icon/user_normal.jpg'
	self.session['me'] = me
	self.session.save()
	self.redirect('/')
