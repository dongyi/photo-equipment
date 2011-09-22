#coding=utf8
import tornado.web

from common.base_httphandler import BaseHandler

class AccountHandler(BaseHandler):
    def get(self, action):
        if action == 'login':
            return self.render('login.html')
        elif action == 'signup':
            return self.render('signup.html')

    def post(self, action):
        if action == 'login':
            return self.redirect('/')
        elif action == 'signup':
            return self.render('/')
