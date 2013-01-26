import webapp2
import jinja2
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.ext import db
import os
from google.appengine.api import search
import logging
import urllib
from google.appengine.api import images
import re
import random
import string
import hmac
from google.appengine.api import mail

#'http://localhost:8080'
domain = 'http://learnmastermentor.appspot.com'

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class User(db.Model):
    username      = db.StringProperty(required = True)
    password_hash = db.StringProperty(required = True)
    email         = db.StringProperty(required = True)
    activated     = db.StringProperty(required = True)
    activation_key= db.StringProperty(required = True)

class ThinDB(db.Model):
    username      = db.StringProperty(required = True)
    asset         = db.StringProperty(required = True)
    asset_key     = db.StringProperty(required = True)
    str_value     = db.StringProperty(required = False)
    int_value     = db.IntegerProperty(required= False)

class Member(db.Model):
    first_name    = db.StringProperty(required = True)
    last_name     = db.StringProperty(required = True)
    email         = db.EmailProperty(required = True)
    headline      = db.TextProperty(required = True)
    active        = db.BooleanProperty(required = True)
    country       = db.StringProperty(required = False)
    city          = db.StringProperty(required = False)
    state         = db.StringProperty(required = False)
    zip_code      = db.StringProperty(required = False)
    linkedin      = db.LinkProperty(required = False)
    facebook      = db.LinkProperty(required = False)
    twitter       = db.StringProperty(required = False)
    skype         = db.StringProperty(required = False)
    blog          = db.LinkProperty(required = False)
    phone         = db.PhoneNumberProperty(required = False)
    username      = db.UserProperty(required = True)
    created_at    = db.DateTimeProperty(auto_now_add = True)
    updated_at    = db.DateTimeProperty(auto_now = True)

class Requestor(db.Model):
    email         =db.EmailProperty(required = True)
    first_name    =db.StringProperty(required = True)
    last_name     =db.StringProperty(required = True)
    country       =db.StringProperty(required = True)
    education     =db.StringProperty(required = False)
    facebook      =db.LinkProperty(required = False)
    linkedin      =db.LinkProperty(required = False)
    twitter       =db.StringProperty(required = False)
    skype         =db.StringProperty(required = False)
    blog          = db.LinkProperty(required = False)
    expertise_sought_name_1     =db.StringProperty(required = True)
    expertise_sought_name_2     =db.StringProperty(required = True)
    expertise_sought_name_3     =db.StringProperty(required = True)
    expertise_name_1            =db.StringProperty(required = True)
    expertise_name_2            =db.StringProperty(required = True)
    expertise_name_3            =db.StringProperty(required = True)
    expertise_name_4            =db.StringProperty(required = False)
    expertise_name_5            =db.StringProperty(required = False)
    expertise_level_1           =db.StringProperty(required = True)
    expertise_level_2           =db.StringProperty(required = True)
    expertise_level_3           =db.StringProperty(required = True)
    expertise_level_4           =db.StringProperty(required = False)
    expertise_level_5           =db.StringProperty(required = False)    
    reason_for_learning         =db.TextProperty(required = False)
    how_they_heard_of_us        =db.TextProperty(required = False)
    learning_style              =db.TextProperty(required = False)
    profession                  =db.TextProperty(required = False)
    current_method              =db.TextProperty(required = True)
    remote_project              =db.TextProperty(required = False)
    created_at    =db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at    =db.DateTimeProperty(required = True,auto_now = True)

#decorator for protecting pages
def login_required(function):
    def _f(self, *args, **kwargs):
        if self.is_logged_in():
            function(self, *args, **kwargs)
        else:
            next_page = self.request.path
            self.redirect('/sign_in?next=%s' %next_page)

    return _f


class SLRequestHandler(webapp2.RequestHandler):
    user = None
    def is_logged_in(self):
        cookie = self.request.cookies.get('user_id')
        if cookie!="" and cookie!=None:
            cookie_split = cookie.split('|')
            user_id = cookie_split[0]
            rand_secret = cookie_split[1]
            hash = cookie_split[2]
            if hmac.new(str(rand_secret), str(user_id)).hexdigest()==str(hash):
                self.user = User.get_by_id(int(user_id))
                return True
            else:
                return False
        else:
            return False


class LandingPageHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        variables = {}
        self.response.out.write(template.render(variables))

class BetaSignUpHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('betasignup.html')
        variables = {}
        self.response.out.write(template.render(variables))

class PodcastHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('innovationintheenterprise.html')
        variables = {}
        self.response.out.write(template.render(variables))

class ProfileHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('publicprofile.html')
        variables = {}
        self.response.out.write(template.render(variables))

class InternalProfileHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('internalprofile.html')
        variables = {}
        self.response.out.write(template.render(variables))

class HumansTxtHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('humans.html')
        variables = {}
        self.response.out.write(template.render(variables))

class SignUpHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('signup.html')
        variables = {}
        self.response.out.write(template.render(variables))

    def post(self):
        email = self.request.get('email')
        username = self.request.get('username')
        password = self.request.get('password')
        username_exists = User.all().filter('username =', username).get()
        if not username_exists:
            #save the new user unactivated
            random_secret = "".join(random.choice(string.letters) for x in xrange(5))
            password_hash = random_secret+'|'+hmac.new(random_secret,password).hexdigest()
            activation_key = hmac.new(random_secret,username).hexdigest()
            new_user = User(email=email,username=username,password_hash=password_hash,activated='False',activation_key=activation_key)
            new_user.put()
            #mail the activation link
            activation_link = domain+'/account_activation?activation_key='+hmac.new(random_secret,username).hexdigest()
            email_template = jinja_environment.get_template('email.html')
            #sender should be a authorised email id.
            #for now use email@anubhavsinha.com
            mail.send_mail(sender="Anubhav Sinha<email@anubhavsinha.com>",
            to=email,
            subject="Activate your Servelife account!",
            body="no html version",
            html=email_template.render({'activation_link':activation_link}))
        template = jinja_environment.get_template('login.html')
        variables = {'email':email}
        self.response.out.write(template.render(variables))

class ActivationHandler(SLRequestHandler):
    def get(self):
        activation_key = self.request.get('activation_key')
        user = User.all().filter('activation_key =', activation_key).get()
        if user:
            user.activated='True'
            user.put()
            self.response.out.write('Your account has been activated!')
        else:
            self.response.out.write('No such activation key!')


class SignInHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('signin.html')
        variables = {}
        self.response.out.write(template.render(variables))

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        user = User.all().filter('email =', email).get()
        if user:
            pass_split = user.password_hash.split('|')
            random_secret = str(pass_split[0])
            password_hash = str(pass_split[1])
            if str(hmac.new(random_secret,password).hexdigest())==str(password_hash):
                user_id =  str(user.key().id())
                #user_id|random_secret|hash
                cookie_value = user_id+'|'+random_secret+'|'+hmac.new(random_secret,user_id).hexdigest()
                cookie = 'user_id = '+cookie_value+';Path = /'
                self.response.headers.add_header('Set-Cookie',cookie)
                self.redirect('/get_user_feed/'+user.username)
            else:
                self.response.out.write('password error!')
        else:
            self.response.out.write('no such email signup with us!')


class LogOutHandler(SLRequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie','user_id=;Path = /')
        self.redirect('/')

class GetUserFeedHandler(SLRequestHandler):
    def get(self, username):
        user = 'mogambo'
        if self.is_logged_in():
            user = self.user
            self.response.out.write('feed from username: '+username+'. Logged in user is:'+user.username)


class GetUserTopicFeedHandler(SLRequestHandler):
    @login_required
    def get(self, username, topic):
        self.response.out.write('feed from username: '+username+' on topic: '+topic)

class AddCourseHandler(SLRequestHandler):
    @login_required
    def get(self):
        #add course form
        pass


app = webapp2.WSGIApplication([('/', LandingPageHandler),
                               ('/betasignup',BetaSignUpHandler),
                               ('/innovationintheenterprise', PodcastHandler),
                               ('/publicprofile', ProfileHandler),
                               ('/internalprofile', InternalProfileHandler),
                               ('/humans.txt', HumansTxtHandler),
                               ('/signup', SignUpHandler),
                               ('/account_activation', ActivationHandler),
                               ('/signin', SignInHandler),
                               ('/logout', LogOutHandler),
                               ('/get_user_feed/(?P<username>.*)', GetUserFeedHandler),
                               ('/get_user_feed_by_topic/(?P<username>.*)/(?P<topic>.*)', GetUserTopicFeedHandler),
                               ('/add_a_course', AddCourseHandler),],
                              debug=True)
