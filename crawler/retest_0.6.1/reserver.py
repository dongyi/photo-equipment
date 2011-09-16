#!/usr/bin/python
#-*- coding: ISO-8859-1 -*-
"""retest
A simple Server which enables tests of Python regular expressions
(re module) in a webbrowser. Uses SimpleHTTPServer and AJAX.

Handles both static application pages (HTML and
javascripts and possibly other text formats) via ``GET`` 
and AJAX calls via ``POST``. Path ``/exit`` is used to stop the server.

:Author: Christof Höke (main developer)
:Author: James Thiele
:License: http://creativecommons.org/licenses/by/2.5/
"""
__version__ = '0.6.1'

import cgi
import re
import threading
import types
import webbrowser

from mimetypes import types_map

import BaseHTTPServer
import SimpleHTTPServer
import os.path

PATH = ''
PORT = 8087
DEFAULTPATH = 'retest.html'
DEFAULTTYPE = "text/html;charset=utf-8"
stop = False
contentTypes = types_map


class ReTestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    
    def sendResponseWithOutput(self, response, contentType, out):
        """
        handles both str and unicode types
        """
        if type(out) is types.UnicodeType:
            out = out.encode('utf-8')
        
        self.send_response(response)
        self.send_header("Content-Type", contentType)
        self.send_header("Content-Length", len(out))
        self.end_headers()
        self.wfile.write(out)
 
    def do_GET(self):
        global stop
        p = str(self.path)[1:]
        if not p:
            p = DEFAULTPATH
        try:
            ## print "path='%s'" % p
            if p == 'exit':
                stop = True
                out = u'bye'
            else:
                out = open(p).read()
            response = 200
            ## print os.path.splitext(p)[1]
            contentType = contentTypes.get(os.path.splitext(p)[1], DEFAULTTYPE)
        except:
            out = u'File not found: %s' % p
            response = 404
            contentType = "text/plain;charset=utf-8"

        self.sendResponseWithOutput(response, contentType, out)

    def _seq2str(self, seq):
        """
        converts sequence of strings or tuples to string to be returned
        to AJAX call
        """
        out = u''
        for toplevel in seq:
            if toplevel is not None:
                if type(toplevel) in types.StringTypes:
                    toplevel = (toplevel, )
                out += u', '.join(
                    ["'%s'" % x.replace("'", "\\'") for x in toplevel])
                out += '\n'
        return out

    def _dict2str(self, d):
        """
        converts dict to string to be returned to AJAX call
        """
        return u''.join([u"%s: '%s'\n" % (k, v) for k, v in d.items()])

    def do_re(self, *args, **params):
        """
        return self._dict2str(params) + '\n' + self._seq2str(params.items())
        """
        txt = unicode(params['txt'], 'utf-8')
        regex = unicode(params['regex'], 'utf-8')
        method = params['method']
        options = re.UNICODE

        optionList = (
             ('dotall', re.DOTALL),
             ('ignorecase', re.IGNORECASE),
             ('multiline', re.MULTILINE),
             ('verbose', re.VERBOSE))

        for s, bitflag in optionList:
            if params.get(s, '') == 'true':
                options |= bitflag

        try:
            cre = re.compile(regex, options)
        except Exception, e:
            out = u'ERROR: %s' % e
        else:
            results = getattr(cre, method)(txt)
            
            if results:
                # list result
                if type(results) == types.ListType:
                    out = self._seq2str(results)
                # match object
                else:
                    out = u'[TEXT MATCHES]\n'
                    ng = self._dict2str(results.groupdict())
                    if ng:
                        out += u'### NAMED GROUPS ###\n%s' % ng
                    g = self._seq2str(results.groups())
                    if g:
                        out += u'### GROUPS ###\n%s' % g
            else:
                out = u'[NO MATCH OR NOTHING FOUND]'
        return out

    def do_POST(self):
        """
        test a re
        """
        length = int(self.headers.getheader('content-length'))        
        qs = self.rfile.read(length)
        params = dict(cgi.parse_qsl(qs, keep_blank_values=1))
        out = self.do_re(**params)
                    
        self.sendResponseWithOutput(200, DEFAULTTYPE, out)


class StoppableHTTPServer(BaseHTTPServer.HTTPServer):
    def serve_forever (self):
        """Handle one request at a time until stopped."""
        global stop
        while not stop:
            self.handle_request()


def run(server_class = StoppableHTTPServer,
        handler_class = ReTestHandler):
    server_address = (PATH, PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()



def openbrowser():
    print "trying to start a browser..."
    print
    webbrowser.open('http://localhost%s:%s' % (PATH, PORT))


# opens a browser after half a second
# remove the next 2 lines if you don't want/need it
t = threading.Timer(0.5, openbrowser)
t.start()

print 'serving on localhost%s:%s' % (PATH, PORT)
print 'stop with CTRL + PAUSE or goto localhost%s:%s/exit' % (PATH, PORT)
print
run()
