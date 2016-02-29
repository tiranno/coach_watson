#!/usr/bin/env python

from watson import Watson
import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.escape

# SERVER APPLICATION
class Application(tornado.web.Application):
    def __init__(self):
        options = tornado.options.options
        watson = Watson(options.watson_user, options.watson_pass)
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static')
        )
        handlers = [
            (r'/about', AboutHandler),
            (r'/', IndexHandler),
            (r'/workout', WorkoutHandler),
            (r'/nutrition', NutritionHandler),
            (r'/ws', WebSocketHandler, {'watson':watson})
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


# ABOUT PAGE HANDLER
class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('about.html')

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)


# PAGE REQUEST HANDLERS
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('_main.html', content='_index.html')

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)


class WorkoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('_main.html', content='_workout.html')

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)


class NutritionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('_main.html', content='_nutrition.html')

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)



class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('WebSocket opened.')

    def check_origin(self, origin):
        return True

    def initialize(self, watson):
        self.watson = watson

    def on_message(self, message):
        # How do I perform a push-up?
        if self.ws_connection:
            print(message)
            answer = self.watson.ask(message)
            self.write_message(tornado.escape.json_encode(answer))

    def on_close(self):
        print('WebSocket closed.')


def main():
    # Define commandline options
    # Serves at http://localhost:8000
    # Usage ./watson_server --watson-user='Bob' --watson-pass='Swordfish'
    tornado.options.define('port', default=8000, help='listen on the given port', type=int)
    tornado.options.define('watson_user', help='user name for the Watson instance')
    tornado.options.define('watson_pass', help='password for the Watson instance')
    tornado.options.parse_command_line()

    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(tornado.options.options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
