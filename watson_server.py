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

from pymongo import MongoClient
from datetime import datetime
import bcrypt


# SERVER APPLICATION
class Application(tornado.web.Application):
    def __init__(self):
        # Global Variables


        # Open connection to Mongo DB
        dbuser = 'HerokuWatson'
        dbpass = 'hweartoskoun'
        client = MongoClient('mongodb://'+dbuser+':'+dbpass+'@ds023458.mlab.com:23458/heroku_6f2n4wp9')
        self.db = client.heroku_6f2n4wp9

        # Server settings
        options = tornado.options.options
        watson = Watson(options.watson_user, options.watson_pass)
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), 'templates'),
            static_path = os.path.join(os.path.dirname(__file__), 'static'),
            cookie_secret = 'cinnamon',
            login_url = '/',
            default_handler_class = fourOhFourHandler
        )
        handlers = [
            # Main Pages
            (r'/', IndexHandler),
            (r'/askwatson', QueryPageHandler),
            (r'/workout', WorkoutHandler),
            (r'/nutrition', NutritionHandler),
            (r'/404', fourOhFourHandler),
            # Websockets
            (r'/ws', WebSocketHandler, {'watson':watson}),
            # User auth post reqs
            (r'/auth/login', LoginHandler),
            (r'/auth/logout', LogoutHandler),
            (r'/auth/register', RegisterHandler),
            # Form validation
            (r'/form/feedback', FeedbackHandler)
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


# Base Handler
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
          return tornado.escape.json_decode(user_json)
        else:
          return None


# PAGE REQUEST HANDLERS
class fourOhFourHandler(BaseHandler):
    def prepare(self):
        self.set_status(404)
        self.render('404.html')

class IndexHandler(BaseHandler):
    def get(self):
        self.render('about.html')

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)

class QueryPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = "Ask Watson"
        self.render('app.html', content='partials/_askwatson.html', title=title)

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)

class WorkoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = "Workout Plan"
        self.render('app.html', content='partials/_workout.html', title=title)

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)

class NutritionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = "Nutrition Plan"
        self.render('app.html', content='partials/_nutrition.html', title=title)

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)


# WEBSOCKET HANDLERS
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('WebSocket opened.')

    def check_origin(self, origin):
        return True

    def initialize(self, watson):
        self.watson = watson

    def on_message(self, message):
        if self.ws_connection:
            print(message)
            answer = self.watson.ask(message)
            # save to db

            # send to user
            self.write_message(tornado.escape.json_encode(answer))

    def on_close(self):
        print('WebSocket closed.')


# USER AUTHENTICATION AND RE.GISTRATION
class LoginHandler(BaseHandler):
    def post(self):
        email = self.get_argument('user-name','')
        password = self.get_argument('user-pass','')
        print('user log in: ' + str(email))

        user = self.application.db['users'].find_one( {'username': email } )

        if user and user['password'] and bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password']:
            self.set_current_user(email)
            self.redirect('/askwatson')
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("incorrect login")
            self.redirect('/' + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

class RegisterHandler(LoginHandler):
    def post(self):
        email = self.get_argument('user-name','')

        in_db = self.application.db['users'].find_one( { 'username': email } )
        if in_db:
            error_msg = u"?error=" + tornado.escape.url_escape("email already taken")
            self.redirect('/' + error_msg)

        password = self.get_argument('user-pass-first','')
        passhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(8).encode('utf-8'))

        user = { }
        user['username'] = email
        user['password'] = passhash
        user['firstname']= self.get_argument('first-name','')
        user['lastname'] = self.get_argument('last-name','')

        auth = self.application.db['users'].insert_one(user).inserted_id
        self.set_current_user(email)

        self.redirect('/askwatson')


# FEEDBACK HANDLER
class FeedbackHandler(BaseHandler):
    def post(self):
        recieved_text = self.get_argument('feedback-text','')

        feedback = { }
        feedback['userid'] = self.get_current_user()
        feedback['text'] = recieved_text
        feedback['url'] = self.request.uri

        fbid = self.application.db['feedback'].insert_one(feedback).inserted_id
        print('feedback recieved with id' + str(fbid))


# QA HISTORY HANDLER
class QAHistoryHandler(BaseHandler):
    def get(self):
        user = self.get_current_user()
        self.application.db['qa-pairs'].find({userid: user}).sort({_id:-1})
        # Need to only get and return ten at a time wrt the latest one loaded

    def post(self):
        qa = { }
        qa['userid'] = self.get_current_user()
        qa['question'] = message
        qa['answer'] = answer
        qa['datetime'] = datetime.isoformat(datetime.utcnow())

        qaid = self.application.db['qa-pairs'].insert_one(qa).inserted_id



def main():
    # Define commandline options
    # Serves at http://localhost:8000
    # Usage ./watson_server --watson-user='Bob' --watson-pass='Swordfish'
    tornado.options.define('port', default=8000, help='listen on the given port', type=int)
    tornado.options.define('watson_user', help='user name for the Watson instance')
    tornado.options.define('watson_pass', help='password for the Watson instance')
    tornado.options.parse_command_line()

    # Start the app
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(int(os.environ.get("PORT", 8000)))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
