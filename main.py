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

domain = 'http://localhost:8080'

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class User(db.Model):
    username      = db.StringProperty(required = True)
    password_hash = db.StringProperty(required = True)
    email         = db.StringProperty(required = True)
    activated     = db.StringProperty(required = True)

class ThinDB(db.Model):
    username      = db.StringProperty(required = True)
    key_          = db.StringProperty(required = True)
    string_value  = db.StringProperty(required = True)
    int_value     = db.IntegerProperty(required= True)


class LandingPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        variables = {}
        self.response.out.write(template.render(variables))


class HumansTxtHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('humans.html')
        variables = {}
        self.response.out.write(template.render(variables))

class SignupHandler(webapp2.RequestHandler):
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
            rand_secret = "".join(random.choice(string.letters) for x in xrange(5))
            password_hash = rand_secret+'|'+hmac.new(rand_secret,password).hexdigest()
            new_user = User(email=email,username=username,password_hash=password_hash,activated='False')
            new_user.put()
            #mail the activation link
            activation_link = domain+'/activate_account?activation_key='+hmac.new(rand_secret,username).hexdigest()
            email_template = jinja_environment.get_template('email.html')
            mail.send_mail(sender="Serve Life<mailbot@servelife.com>",
            to=email,
            subject="Activate your Servelife account!",
            body="no html version",
            html=email_template.render({'activation_link':activation_link}))
        template = jinja_environment.get_template('login.html')
        variables = {'email':email}
        self.response.out.write(template.render(variables))


app = webapp2.WSGIApplication([('/', LandingPageHandler),
                               ('/humans.txt', HumansTxtHandler),
                               ('/signup', SignupHandler),],
                              debug=True)
