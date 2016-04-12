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
from bson import ObjectId
import bcrypt


# SERVER APPLICATION
class Application(tornado.web.Application):
    def __init__(self):

        # Open connection to Mongo DB
        dbuser = 'HerokuWatson'
        dbpass = 'hweartoskoun'
        client = MongoClient('mongodb://' + dbuser + ':' + dbpass + '@ds023458.mlab.com:23458/heroku_6f2n4wp9')
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
            (r'/', AboutHandler),
            (r'/askwatson', QueryPageHandler),
            (r'/workout', WorkoutHandler),
            (r'/workout/day', WorkoutDayHandler),
            (r'/nutrition', NutritionHandler),
            (r'/profile', ProfileHandler),
            (r'/404', fourOhFourHandler),
            # Websockets
            (r'/ws', WebSocketHandler, {'watson':watson}),
            # Qusetion/Answer
            (r'/qahistory', QAHandler),
            # S2T
            (r'/speech_to_text', S2THandler),
            # User auth post reqs
            (r'/auth/login', LoginHandler),
            (r'/auth/logout', LogoutHandler),
            (r'/auth/register', RegisterHandler),
            # Form validation
            (r'/form/feedback', FeedbackHandler),
            (r'/(.*)', fourOhFourHandler)
        ]
        tornado.web.Application.__init__(self, handlers, **settings)


### BASE HANDLER ###
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
          return tornado.escape.json_decode(user_json)
        else:
          return None

    def get_current_userid(self):
        user_json = self.get_secure_cookie("userid")
        if user_json:
          return tornado.escape.json_decode(user_json)
        else:
          return None


### 404 page and related handlers ###
class fourOhFourHandler(BaseHandler):
    def prepare(self):
        self.set_status(404)
        self.render('404.html')


### INFORMATION pages and related handlers ###
class AboutHandler(BaseHandler):
    def get(self):
        if self.get_current_userid() != None:
            self.redirect('/askwatson')
        self.render('about.html')

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)


### ASK WATSON page and related handlers ###
class QueryPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = "Ask Watson"
        self.render('app.html', content='partials/_askwatson.html', title=title)

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)

# QA history handler
class QAHandler(BaseHandler):
    def get(self):
        #Need to get x amount to return
        user_json = self.get_secure_cookie("userid")
        if user_json:
            userid = tornado.escape.json_decode(user_json)

            pairs = self.application.db['qa-pairs'].find({'userid': userid}).sort('_id', -1).limit(10)

            p_arr = []
            for pair in pairs:
                p = { }
                p['qaid'] = str( pair['_id'] )
                p['question'] = pair['question']
                p['answer'] = pair['answer']
                p_arr.append(p)
            self.write(tornado.escape.json_encode( p_arr ))


    def post(self):
        qa = { }
        qa['userid'] = self.get_current_userid()
        qa['question'] = message
        qa['answer'] = answer
        qa['datetime'] = datetime.isoformat(datetime.utcnow())

        qaid = self.application.db['qa-pairs'].insert_one(qa).inserted_id

# Speech-to-text handler
class S2THandler(BaseHandler):
    def get(self):
        self.write(Watson.get_S2T_token())

# websocket handler
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print('WebSocket opened.')

    def initialize(self, watson):
        self.watson = watson

    def on_message(self, message):
        if self.ws_connection:
            print(message)

            # add timeout?
            answer = self.watson.ask(message)
            # save to db
            user_json = self.get_secure_cookie("userid")
            if user_json and answer:
                userid = tornado.escape.json_decode(user_json)
                #QA post
                qa = { }
                qa['userid'] = userid
                qa['question'] = message
                qa['answer'] = answer

                qa['datetime'] = datetime.isoformat(datetime.utcnow())
                print 'y'
                self.application.db['qa-pairs'].insert_one(qa)

            # send to user
            self.write_message(tornado.escape.json_encode(answer))

    def on_close(self):
        print('WebSocket closed.')

    def ping(self):
        pass

    def on_pong(self):
        pass



### WORKOUT page and related handlers ###
class WorkoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = "Workout Plan"
        self.render('app.html', content='partials/_workout.html', title=title)

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)

# workout day handler
class WorkoutDayHandler(WorkoutHandler):
    def get(self):
        user_json = self.get_secure_cookie("userid")
        if user_json:
            userid = tornado.escape.json_decode(user_json)
            dayid = self.get_argument('dayid','')
            day_plan = self.application.db['workout-plans'].find({'userid': userid, 'dayid': dayid})

            exer_arr = []
            for exercise in day_plan:
                e = { }
                e['exerid'] = str( exercise['_id'] )
                e['name'] = exercise['name']
                e['amount'] = exercise['amount']
                exer_arr.append(e)

            self.write(tornado.escape.json_encode( exer_arr ))


    def post(self):
        user_json = self.get_secure_cookie("userid")

        exer = {}
        exer['userid'] = tornado.escape.json_decode(user_json)
        exer['dayid'] = self.get_argument('dayid','')
        exer['name'] = self.get_argument('exer-name','')
        exer['amount'] = self.get_argument('exer-amnt','')

        self.application.db['workout-plans'].insert_one(exer)

    def put(self):
        pass

    def delete(self):
        pass


### NUTRITION page and related handlers ###
class NutritionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = "Nutrition Plan"
        self.render('app.html', content='partials/_nutrition.html', title=title)

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)


### PROFILE page and related handles ###
class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        title = "Profile"

        user_json = self.get_secure_cookie("userid")
        if user_json:
            userid = tornado.escape.json_decode(user_json)
            user = self.application.db['users'].find_one({'_id': ObjectId(userid)})
            email = user['username']
            first = user['firstname']
            last = user['lastname']

            self.render('app.html', content='partials/_profile.html', title=title,
                first=first, last=last, email=email)
        else:
            return None

    def post(self):
        email = self.get_argument('user-name','')

        user = { }

        self.application.db['users'].update()
        self.redirect('/askwatson')

    def write_error(self, status_code, **kwargs):
        self.write('Oops, a %d error occurred!\n' % status_code)


### USER AUTHENTICATION and REGISTRATION handlers ###
class LoginHandler(BaseHandler):
    def post(self):
        email = self.get_argument('user-name','')
        password = self.get_argument('user-pass','')
        print('user log in: ' + str(email))

        user = self.application.db['users'].find_one( {'username': email } )

        if user and user['password'] and bcrypt.hashpw(password.encode('utf-8'), user['password'].encode('utf-8')) == user['password']:
            self.set_current_user(user)
            self.redirect('/askwatson')
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("incorrect login")
            self.redirect('/' + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode( user["firstname"]+" "+user["lastname"] ))
            self.set_secure_cookie("userid", tornado.escape.json_encode( str(user["_id"]) ))
        else:
            self.clear_cookie("user")
            self.clear_cookie("userid")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.clear_cookie("userid")
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

        self.application.db['users'].insert_one(user)
        user = self.application.db['users'].find_one( { 'username': email } )
        self.set_current_user( user )

        self.redirect('/askwatson')


### FEEDBACK HANDLER ###
class FeedbackHandler(BaseHandler):
    def post(self):
        recieved_text = self.get_argument('feedback-text','')

        feedback = { }
        feedback['userid'] = self.get_current_userid()
        feedback['text'] = recieved_text
        feedback['url'] = self.request.uri

        fbid = self.application.db['feedback'].insert_one(feedback).inserted_id
        print('feedback recieved with id' + str(fbid))



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
