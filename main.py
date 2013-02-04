import webapp2
import jinja2

import os
import random
import string
import hmac
from google.appengine.api import mail
from models.models import *

#'http://localhost:8080'
domain = 'http://learnmastermentor.appspot.com'

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'views')))


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

class UserProfileHandler(SLRequestHandler):
    def get(self, username):
        template = jinja_environment.get_template('publicprofile.html')
        variables = {'username': username}
        self.response.out.write(template.render(variables))



class TeamProfileHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('teampublicprofile.html')
        variables = {}
        self.response.out.write(template.render(variables))

class ProjectProfileHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('projectpublicprofile.html')
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
            try:
                mail.send_mail(sender="Alan Ruth<alan@notionlabs.com>",
                to=email,
                subject="Activate your Servelife account!",
                body="no html version",
                html=email_template.render({'activation_link':activation_link}))
            except:
                self.response.out.write('mail config not working..')

            template = jinja_environment.get_template('login.html')
            variables = {'email':email}
            self.response.out.write(template.render(variables))
        self.response.out.write('this username not available')

class ActivationHandler(SLRequestHandler):
    def get(self):
        activation_key = self.request.get('activation_key')
        user = User.all().filter('activation_key =', activation_key).get()
        if user:
            user.activated='True'
            user.put()
            username = user.username
            user_influence = UserThinDB(username=username,
                                    asset= 'profile',
                                    asset_key= 'influence',
                                    str_value= '',
                                    int_value= 100)
            user_influence.put()
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
                               ('/userprofile/(?P<username>.*)', UserProfileHandler),
                               ('/teamprofile/(?P<team>.*)', TeamProfileHandler),
                               ('/projectprofile/(?P<project>.*)', ProjectProfileHandler),
                               ('/signup', SignUpHandler),
                               ('/account_activation', ActivationHandler),
                               ('/signin', SignInHandler),
                               ('/logout', LogOutHandler),
                               ('/get_user_feed/(?P<username>.*)', GetUserFeedHandler),
                               ('/get_user_feed_by_topic/(?P<username>.*)/(?P<topic>.*)', GetUserTopicFeedHandler),
                               ('/add_a_course', AddCourseHandler),],
                              debug=True)
