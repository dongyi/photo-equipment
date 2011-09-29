#coding=utf8
import tornado.web
import tornado.database

from common.base_httphandler import BaseHandler

def check_user(email, password):
    pass

def qn(s):
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%"]
    for stuff in dirty_stuff:
        s = s.replace(stuff,"")
    return "'"+s+"'"

class AccountHandler(BaseHandler):
    def get(self, action):
        f = lambda x:self.get_argument(x, '').strip()
        name = f('name')
        password = f('password')
        if action == 'login':
            return self.render('login.html')
        elif action == 'signup':
            return self.render('signup.html', site='sina')
        elif action == 'logout':
            self.session.clear()
            self.session.save()
            self.redirect('/')

    def post(self, action):
        f = lambda x:self.get_argument(x, '').strip()
        if action == 'login':
            user = self.db.get('select * from account where name=%s and password=PASSWORD(%s)'%(qn(name), qn(password))) # this will raise error if not exist
            self.session['user'] = dict(name=user.name, id=user.id)
            self.session.save()
            return self.redirect('/')
        elif action == 'signup':
            name = f('name')
            email = f('email')
            password = f('password')
            self.db.execute('INSERT INTO account (name, email, password) VALUES(%s, %s, MD5(%s))'%(qn(name), qn(email), qn(password)))
            return self.render('/')
