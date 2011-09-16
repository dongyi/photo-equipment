#coding=utf8
import tornado.web
import tornado.httpserver
import tornado.httpclient

import os
import re
import urllib2

from urlparse import urljoin
from tornado.options import options
#from config.web_config import PLATFORM


from httputil import iri_to_uri

#from config.web_config import PLATFORM

absolute_http_url_re = re.compile(r"^https?://", re.I)


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)
        self.path = ''

    def get_host(self):
        """Returns the HTTP host using the environment or request headers."""
        return self.request.headers.get('Host')

    def build_absolute_uri(self, location=None):
        """
        Builds an absolute URI from the location and the variables available in
        this request. If no location is specified, the absolute URI is built on
        ``request.get_full_path()``.
        """
        if not location:
            location = ''
        if not absolute_http_url_re.match(location):
            current_uri = '%s://%s%s' % (self.is_secure() and 'https' or 'http',
                                         self.get_host(), self.path)
            location = urljoin(current_uri, location)
        return iri_to_uri(location)

    def is_secure(self):
        return os.environ.get("HTTPS") == "on"

    def get_error_html(self, status_code, exception=None, **kwargs):
        return self.render_string('_error.htm', status_code=status_code, exception=exception, **kwargs)


class ReqMixin(object):
    user_callback = {}

    def wait_for_request(self, callback):
        cls = ReqMixin
        cls.user_callback.update({self.get_user_id():callback})

    def new_req(self, req):
        cls = ReqMixin
        callback = cls.user_callback[self.get_user_id()]
        callback(req)

class ProxyHandler(BaseHandler, ReqMixin):
    @tornado.web.asynchronous
    def get(self, action):
        if action == 'update':
            self.wait_for_request(self.async_callback(self.send))

        elif action == 'request':
            http = tornado.httpclient.AsyncHTTPClient()
            http.fetch(self.get_argument('url'), callback=self.new_req)
            self.finish()


    def send(self, response):
        # Closed client connection
        if response.error:
            raise tornado.web.HTTPError(500)
        self.write(response.body)
        self.flush()

