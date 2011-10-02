#coding=utf8

import tornado.web
from common.base_httphandler import BaseHandler


def qn(s):
    # 防止sql注入
    dirty_stuff = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%"]
    for stuff in dirty_stuff:
        s = s.replace(stuff,"")
    return "'"+s+"'"

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
        elif action == 'check_user':
            # 从微博,人人,豆瓣登录过来的请求最后重定向到这里,检查用户是否在本站注册过,注册过就再重定向到首页,否则render到注册页面
            platform = self.session.get('platform', '')
            site_username = self.session.get('site_username', '')
            site_id = self.session.get('site_id', '') #TODO: 在connect下的各个登录模块中把session中存的内容加上这3个, 统一处理
            if platform == 'weibo':
                sql = 'select count(*) from account where weiboid=%d'%int(site_id)
            elif platform == 'douban':
                sql = 'select count(*) from account where doubanid=%d'%int(site_id)
            elif platform == 'renren':
                sql = 'select count(*) from account where renrenid=%d'%int(site_id)
            count = self.db.get(sql)
            if count == 0:
                return self.render('signup.html', platform=platform, site_username=site_username) # TODO: 更新signup模版显示用户是从哪里来的
            elif count == 1:
                return self.redirect('/')
            else:
                raise tornado.web.HTTPError(500, 'more than 1 account found')


    def post(self, action):
        f = lambda x:self.get_argument(x, '').strip()
        name = f('name')
        password = f('password')
        if action == 'login':
            user = self.db.get('select * from account where username=%s and password=PASSWORD(%s)'%(qn(name), qn(password))) # this will raise error if not exist
            self.session['user'] = dict(name=user.username, id=user.id)
            self.session.save()
            return self.redirect('/')
        elif action == 'signup':
            name = f('name')
            email = f('email')
            password = f('password')
            self.db.execute('INSERT INTO account (username, email, password) VALUES(%s, %s, MD5(%s))'%(qn(name), qn(email), qn(password)))
            return self.redirect('/')
