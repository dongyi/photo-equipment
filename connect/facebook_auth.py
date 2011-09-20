#coding=utf8
import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from common.base_httphandler import BaseHandler


class MainHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)


    @tornado.web.asynchronous
    @tornado.web.authenticated
    def get(self):
        self.facebook_request("/me/home", self._on_stream,
                              access_token=self.current_user["access_token"])

        def _on_stream(self, stream):
            if stream is None:
                # Session may have expired
                self.redirect("/auth/login")
                return
            self.render("stream.html", stream=stream)



class AuthLoginHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)


    @tornado.web.asynchronous
    def get(self):
        my_url = (self.request.protocol + "://" + self.request.host +
                  "/auth/login?next=" +
                  tornado.escape.url_escape(self.get_argument("next", "/")))
        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=my_url,
                client_id=options.facebook_api_key,
                client_secret=options.facebook_secret,
                code=self.get_argument("code"),
                callback=self._on_auth)
            return
        self.authorize_redirect(redirect_uri=my_url,
                                client_id=options.facebook_api_key,
                                extra_params={"scope": "read_stream"})

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Facebook auth failed")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))

class AuthLogoutHandler(BaseHandler, tornado.auth.FacebookGraphMixin):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))
