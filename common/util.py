#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time
import urllib
import memcache

try:
    import ujson as json
except:
    import json
#import pdb
import types

from datetime import date, datetime

# load all config files


import tornado.database

from config.membase_config import mc_list, mb_list, user_dbconfig_mc_addr, public_mc, lock_mc_addr


MASTER_DB_FLAG = 0
SLAVE_DB_FLAG = 1
LOG_MAX_COUNT = 4

srv_count = len(mc_list)

def lock(key):
    mc = get_mc_with_info(lock_mc_addr)
    return mc.add(str(key), 1, 1)

def unlock(key):
    mc = get_mc_with_info(lock_mc_addr)
    return mc.delete(str(key))

def get_public_mc():
    return memcache.Client(public_mc)


def get_mc(persistence=False):
    """
    获取与memcache的连接

    @param long userid : 玩家的guid

    @return : Fmemcache instance
    """
    return memcache.Client(mb_list) if persistence else memcache.Client(mc_list)


def get_center_mc():
    """
    获取玩家数据库信息memcache的连接

    @return : Fmemcache instance
    """

    return memcache.Client(user_dbconfig_mc_addr)


def get_mc_with_info(mcinfo):
    """
    通过信息获取memcache的连接

    @param list mcinfo : memcache的连接信息

    @return : Fmemcache instance
    """
    return memcache.Client(mcinfo)


def is_in_same_day(argtime):
    """
    判断argtime和当前时间是否是否在同一天内

    @return : True or False
    """

    now = int(time.time())
    kDaySeconds = 24 * 3600
    return (argtime / kDaySeconds) == (now / kDaySeconds)
    #return (now-argtime)/kDaySeconds == 0


def my_json_decoder(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r is not JSON serializable' % obj)


class Promise(object):
    pass

def smart_str(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Returns a bytestring version of 's', encoded as specified in 'encoding'.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if isinstance(s, Promise):
        return unicode(s).encode(encoding, errors)
    elif not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return ' '.join([smart_str(arg, encoding, strings_only,
                        errors) for arg in s])
            return unicode(s).encode(encoding, errors)
    elif isinstance(s, unicode):
        return s.encode(encoding, errors)
    elif s and encoding != 'utf-8':
        return s.decode('utf-8', errors).encode(encoding, errors)
    else:
        return s

def iri_to_uri(iri):
    """
    Convert an Internationalized Resource Identifier (IRI) portion to a URI
    portion that is suitable for inclusion in a URL.

    This is the algorithm from section 3.1 of RFC 3987.  However, since we are
    assuming input is either UTF-8 or unicode already, we can simplify things a
    little from the full method.

    Returns an ASCII string containing the encoded result.
    """
    # The list of safe characters here is constructed from the "reserved" and
    # "unreserved" characters specified in sections 2.2 and 2.3 of RFC 3986:
    #     reserved    = gen-delims / sub-delims
    #     gen-delims  = ":" / "/" / "?" / "#" / "[" / "]" / "@"
    #     sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
    #                   / "*" / "+" / "," / ";" / "="
    #     unreserved  = ALPHA / DIGIT / "-" / "." / "_" / "~"
    # Of the unreserved characters, urllib.quote already considers all but
    # the ~ safe.
    # The % character is also added to the list of safe characters here, as the
    # end of section 3.1 of RFC 3987 specifically mentions that % must not be
    # converted.
    if iri is None:
        return iri
    return urllib.quote(smart_str(iri), safe="/#%[]=:;$&()+,!?*@'~")

def dict2xml_iter(d):
    for k, v in d.iteritems():
        output = '<%s>'%str(k)
        output += '\n'
        for attr, val in v.items():
            output += '  <%s>'%str(attr)
            output += ' ' + str(val)
            output += '  </%s>'%str(attr)
            output += '  \n'
        output += '</%s>'%str(k)
        yield output

def dict2xml(d):
    return '\n'.join(dict2xml_iter(d))
