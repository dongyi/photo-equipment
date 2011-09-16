#coding=utf8

from common.base_httphandler import BaseHandler
from weibopy import OAuthHandler
from tornado.options import options
from weibopy.api import API

try:
    import cjson as json
except ImportError:
    import json

class ShareHandler(BaseHandler):
    def post(self, site):
        if site == 'wb':
            content = self.get_argument('content')
            access_token = self.session.get('oauth_access_token')
            auth = OAuthHandler(options.SINA_APP_KEY, options.SINA_APP_SECRET)
            auth.set_access_token(access_token.key, access_token.secret)
            api = API(auth)
            api.update_status(content)
            self.finish(json.dumps('success'))
            #self.finish()
