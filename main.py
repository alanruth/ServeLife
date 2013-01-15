import webapp2
import jinja2
import os
import re
import random
import string
import json


from PIL import Image
import StringIO
from mimetypes import guess_type
from google.appengine.api import files
from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.api import urlfetch
import cStringIO
import urllib2,urllib
from google.appengine.api import images

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class LandingPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('home.html')
        variables = {}
        self.response.out.write(template.render(variables))


app = webapp2.WSGIApplication([('/', LandingPageHandler),],
                              debug=True)
