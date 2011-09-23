#coding=utf8
import tornado.web
import tornado.database

from common.base_httphandler import BaseHandler

def new_user(name, password, email):
    pass

def check_user(email, password):
    pass

class AccountHandler(BaseHandler):
    def get(self, action):
        if action == 'login':
            return self.render('login.html')
        elif action == 'signup':
            return self.render('signup.html', site='sina')
        elif action == 'logout':
            self.session.clear()
            self.session.save()
            self.redirect('/')

    def post(self, action):
        if action == 'login':
            return self.redirect('/')
        elif action == 'signup':
            name = self.get_argument('name')
            email = self.get_argument('email')
            password = self.get_argument('password')
            return self.render('/')
