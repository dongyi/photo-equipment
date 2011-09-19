#!//usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import hashlib
import time
import urllib
import json
import memcache
from tornado.options import options

from common.base_httphandler import BaseHandler
from config.membase_config import session_mc
session_mc_client = memcache.Client(session_mc)

RENREN_AUTHORIZATION_URI = "http://graph.renren.com/oauth/authorize"
RENREN_ACCESS_TOKEN_URI = "http://graph.renren.com/oauth/token"
RENREN_SESSION_KEY_URI = "http://graph.renren.com/renren_api/session_key"
RENREN_API_SERVER = "http://api.renren.com/restserver.do"

def _get_referer_url(request_handle):
    headers = request_handle.request.headers
    referer_url = headers.get('HTTP_REFERER', '/')
    host = headers.get('Host')
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/' # 避免外站直接跳到登录页而发生跳转错误
        return referer_url

class LoginCheckHandler(BaseHandler):
    def get(self):
        if self.get_argument('code', None):
            code = self.get_argument('code')
            login_backurl = self.build_absolute_uri('/rrlogincheck')
            R = renren()
            url = R.second(login_backurl, code)
            access_token = url['access_token']
            self.session['oauth_access_token'] = access_token
            session_key_list = R.third(access_token)
            uid = session_key_list['user']['id']
            session_key = session_key_list['renren_token']['session_key']
            infoma = R.fourth(session_key, uid)
            self.set_cookie('sid', self.session.session_id)
            self.set_cookie('uid', str(uid))
            self.session['me'] = infoma
            self.session['username'] = infoma.name
            self.session['platform'] = 'renren'
            self.session.save()
            session_mc_client.set(str(uid), self.session.session_id)
            back_to_url = self.session.get('login_back_to_url','/')
            return self.redirect(back_to_url)

class LoginHandler(BaseHandler):
    def get(self):
        login_backurl = self.build_absolute_uri('/rrlogincheck')
        R = renren()
        url = R.first(login_backurl)
        self.redirect(url)

class LogoutHandler(BaseHandler):
    def get(self):
        self.session.clear()
        self.session.save()
        back_to_url = _get_referer_url(self)
        self.redirect(back_to_url)

class renrenuser:
    def __init__(self, id, name, img):
        self.id = id
        self.name = name
        self.url = 'http://www.renren.com/home#/home?id=%s'%id
        self.profile_image_url = img

def hash_params(params,secrect_key):
    hasher = hashlib.md5("".join(["%s=%s"%(x,params[x]) for x in sorted(params.keys())]))
    hasher.update(secrect_key)
    return hasher.hexdigest()

class renren:
    def first(self, redirect, response_type='code'):
        params = {}
        params['client_id'] = options.RENREN_APP_API_KEY
        params['response_type'] = response_type
        params['redirect_uri'] = redirect
        params = urllib.urlencode(params)
        url = RENREN_AUTHORIZATION_URI+'?'+params
        return url
    def second(self, redirect, code, grant_type='authorization_code', response_type='code', client_id=options.RENREN_APP_API_KEY, client_secret=options.RENREN_APP_SECRET_KEY):
        params = {}
        params['client_id'] = client_id
        params['client_secret'] = client_secret
        params['response_type'] = response_type
        params['redirect_uri'] = redirect
        params['grant_type'] = grant_type
        params['code'] = code
        params = urllib.urlencode(params)
        url = RENREN_ACCESS_TOKEN_URI+'?'+params
        f = urllib.urlopen(url)
        line = f.read()
        info = json.loads(line)
        return info
    def third(self,access_token):
        params = {}
        params['oauth_token'] = access_token
        params = urllib.urlencode(params)
        url = RENREN_SESSION_KEY_URI+'?'+params
        f = urllib.urlopen(url)
        line = f.read()
        info = json.loads(line)
        return info
    def fourth(self,session_key,id):
        params = {}
        params = {"method": "users.getInfo", "fields": "name,tinyurl"}
        params['session_key'] = session_key
        params["api_key"] = options.RENREN_APP_API_KEY
        params["call_id"] = str(int(time.time() * 1000))
        params["format"] = "json"

        params["v"] = '1.0'
        sig = hash_params(params, options.RENREN_APP_SECRET_KEY)
        params["sig"] = sig
        params = urllib.urlencode(params)
        f = urllib.urlopen(RENREN_API_SERVER, params).read()
        info = json.loads(f)
        if type(info) is list:
            info = info[0]
        ren = renrenuser(id, info['name'], info['tinyurl'])
        return ren


def main():
    R = renren()
    url = R.first(options.RENREN_APP_API_KEY,'http://graph.renren.com/oauth/login_success.html')
    res = urllib.urlopen(url)
    print res.read()


if "__main__" == __name__:
    main()




