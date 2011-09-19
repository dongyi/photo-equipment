#coding=utf8

#system modules:
import sys
import os

#tornado modules:
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload

import common.session
import config.web_config

#controllers:
from common.base_httphandler import BaseHandler
from common.base_httphandler import ProxyHandler
from connect.sina_auth import  AuthLoginHandler, AuthLoginCheckHandler, AuthLogoutHandler
from connect.renren_auth import LoginHandler as RRLoginHandler
from connect.renren_auth import LogoutHandler as RRLogoutHandler
from connect.renren_auth import LoginCheckHandler as RRLoginCheckHandler
from connect.douban_auth import LoginHandler as DBLoginHandler
from connect.douban_auth import LoginCheckHandler as DBLoginCheckHandler
from connect.douban_auth import LogoutHandler as DBLogoutHandler
from connect.facebook_auth import AuthLoginHandler as FBAuthLoginHandler
from connect.facebook_auth import AuthLogoutHandler as FBAuthLogoutHandler

from equip import EquipmentHandler, EquipmentListHandler

class MainHandler(BaseHandler):
    def get(self):
        self.render('about.html')
class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

settings = dict(
                cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
                debug=True,
                session_secret='some secret password!!',
                session_dir='sessions',
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                xsrf_cookies=False,
            )

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r'/login', LoginHandler),
            (r'/proxy/(.*)', ProxyHandler),
            (r'/equipment_list/(.*)', EquipmentListHandler),
            (r'/equipment/(.*)', EquipmentHandler),
            (r"/wblogin", AuthLoginHandler),
            (r"/wblogout", AuthLogoutHandler),
            (r"/wblogin_check", AuthLoginCheckHandler),
            (r"/rrlogin", RRLoginHandler),
            (r"/rrlogout", RRLogoutHandler),
            (r'/rrlogincheck', RRLoginCheckHandler),
            (r"/dblogin", DBLoginHandler),
            (r"/dblogout", DBLogoutHandler),
            (r'/dblogincheck', DBLoginCheckHandler),
            (r'/fblogin', FBAuthLoginHandler),
            (r'/fblogout', FBAuthLogoutHandler),
            ]
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = common.session.TornadoSessionManager(settings["session_secret"], settings["session_dir"])

def main(port):
    tornado.options.parse_command_line()
    print "start on port %s..."%port

    app = Application()
    app.listen(port)
    if True:
        application = tornado.ioloop.IOLoop.instance()
        tornado.autoreload.start(application)
        application.start()
    else:
        tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
    else:
        port = tornado.options.options.port
    main(int(port))
