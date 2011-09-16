#coding=utf8
import re
import time
import memcache
import tornado.web
import traceback


from config.web_config import PLATFORM
from config.web_config import ADMIN_LIST

from config.membase_config import lock_mc_addr

INTERNAL_IP_PATTERN = re.compile('127.0.0.1|192.168.*.*')

def login_required(func):
    def new_func(*argc, **argkw):
        # check if the user logined
        request = argc[0] or argkw.get('request')
        if PLATFORM == 'sina':
            access_token = request.session.get('oauth_access_token')
            if access_token is None:
                return request.render("login.html")
            return func(*argc, **argkw)
        elif PLATFORM == 'renren':
            return func(*argc, **argkw)
        elif PLATFORM == 'qq':
            return func(*argc, **argkw)
    return new_func

def admin_required(func):
    def new_func(*argc, **argkw):
        # FIXME only for dev
        return func(*argc, **argkw)
        request = argc[0] or argkw.get('request')
        userid = request.get_user_id()
        if userid not in ADMIN_LIST:
            raise tornado.web.HTTPError(500, 'this user is not administrator, please contact dongyi\n' + traceback.format_exc())
        return func(*argc, **argkw)
    return new_func

def internal(func):
    # only allow interal http request
    def new_func(*argc, **argkw):
        request = argc[0] or argkw.get('request')
        if INTERNAL_IP_PATTERN.match(request.request.remote_ip):
            return func(*argc, **argkw)
        else:
            raise Exception('not from internal')
    return new_func



def method_lock(func, key):
    """ Usage:
    @method_lock('lock_key')
    def auction():
        do_something
    """
    def method_wrapper(func):
        def new_func(*argc, **argkw):
            lock_mc = memcache.Client(lock_mc_addr)
            if not lock_mc.add(key, 1, 1):
                if not lock_mc.add(key, 1, 1):
                    if not lock_mc.add(key, 1, 1):
                        raise
            func(*argc, **argkw)
            lock_mc.delete(key)
        return new_func
    return method_wrapper


def log_and_profile(log_level=[]):
    def method_wrapper(func):
        def new_func(*argc, **argkw):

            request = argc[0] or argkw.get('request')
            remote_ip = request.request.remote_ip
            uri = request.request.uri
            method = request.request.method
            userid = request.get_user_id()
            start = time.time()
            arguments = {}
            headers = {}

            try:
                func(*argc, **argkw)
            except:
                raise tornado.web.HTTPError(500, traceback.format_exc().replace('\n', '<br><br>').replace('%', '^'))
            if 'arg' in log_level:
                arguments = request.request.arguments
            if 'headers' in log_level:
                headers = request.request.headers
            excute_time = time.time() - start
            log_text = 'userid:%d from %s %s %s , consume:%s, arguments:%s, headers:%s'%(userid, remote_ip, method, uri, excute_time, str(arguments), str(headers))
            print log_text
        return new_func
    return method_wrapper
