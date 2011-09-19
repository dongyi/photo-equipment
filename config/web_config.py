#coding=utf8

import os

from tornado.options import define

define('debug', default=True)
define("port", default=8888, help="run on the given port", type=int)

# sina options:
define("SINA_APP_KEY", default="911987553", help="sina_app_key")
define("SINA_APP_SECRET", default="003f2405df0317bbf8380ff65213b0a6", help="SINA_APP_SECRET")

# facebook options:
define("facebook_api_key", help="your Facebook application API key",
              default="141227072611460")
define("facebook_secret", help="your Facebook application secret",
              default="537a73968e1b2bf5200099d75d8bed17")

# renren options:
define('RENREN_APP_API_KEY', default='fc39a39382304aeca966de940af253e5')
define('RENREN_APP_SECRET_KEY', default='922227ccf2144ba7995c4f53be0798b8')

# qq options:
appid = 18196
appkey = '65501caeb2da4ce78d28544b0ab3eeaa'
appname = 'app18196'

# douban options:
define('douban_api_key', default='07bbe3235f73a1a81733a96a1e5ae4f8')
define('douban_api_secret', default='8c40842909ab7e83')

define("pengyou_app_id", default=18196, help="pengyou.com app id")
define("pengyou_app_key", default="65501caeb2da4ce78d28544b0ab3eeaa", help="pengyou.com app key")
define("pengyou_app_name", default="app18196", help="pengyou.com app name")
define("pg_host", help="postgres database host")
define("pg_database", help="postgres database database")
define("pg_user", help="postgres database user")
define("pg_password", help="postgres database password")


# remove '/config'
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))[:-6]

#print PROJECT_ROOT
IMAGE_ROOT = '/static/img/'


UPLOAD_DIR = PROJECT_ROOT + 'static'
PLATFORM = 'sina'


ADMIN_LIST = [1659901275, 1751091154]
# 服务器列表
server_list = ['192.168.0.106', '192.168.0.105']

MAX_PACKAGE_COUNT = 100
