#!/usr/bin/env python

from bob import Bob
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.escape

from tornado.options import define, options
from tornado import gen

# Define commandline options
# Serves at http://localhost:8000
define('port', default=8000, help='listen on the given port', type=int)

class Application(tornado.web.Application):

    def __init__(self):
        bob = Bob()
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static')
        )
        handlers = [
            (r'/', IndexHandler),
            (r'/ws', WebSocketHandler, dict(bob=bob))
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        print('WebSocket opened.')
        self.write_message('Welcome!')

    def check_origin(self, origin):
        return True

    def initialize(self, bob):
        self.bob = bob

    def on_message(self, message):
        if self.ws_connection:
            print(message)
            self.write_message(self.bob.ask(message))

    def on_close(self):
        print('WebSocket closed.')


def main():
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
