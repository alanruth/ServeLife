import webapp2
import jinja2
import os
import random
import string
import hmac
from google.appengine.api import mail
from models.models import *
import json
import urllib, hashlib

#'http://localhost:8080'
domain = 'http://learnmastermentor.appspot.com'

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'views')))

#utility function to get gravatar image url
def get_gravatar_url(size, email):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':'monsterid', 's':str(size)})
    return gravatar_url

#decorator for protecting pages
def login_required(function):
    def _f(self, *args, **kwargs):
        if self.is_logged_in():
            function(self, *args, **kwargs)
        else:
            next_page = self.request.path
            self.redirect('/signin?next=%s' %next_page)

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


class PodcastHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('innovationintheenterprise.html')
        variables = {}
        self.response.out.write(template.render(variables))


class UserProfileNewHandler(SLRequestHandler):

    @login_required
    def get(self, username):
        if self.is_logged_in():
            user = self.user
            #profileinfo is a json string with keys name, title and about
            profile = UserThinDB.all().filter('username = ', user.user_name).filter('asset =', 'profile').filter('asset_key =', 'info').get()
            # print profile.str_value
            profileinfo='{}'
            if profile:
                profileinfo=profile.str_value


            """
            variables = {'name': name,
                         'title': title,
                         'about':about}
            """

            variables = json.loads(profileinfo)
            template = jinja_environment.get_template('newuserprofile.html')
            self.response.out.write(template.render(variables))
        else:
            self.redirect('/signin')

    @login_required
    def post(self, username):
        if self.is_logged_in():
            user = self.user
            first_name = self.request.get('first_name')
            last_name = self.request.get('last_name')
            country = self.request.get('country')
            city = self.request.get('city')
            linkedin_url = self.request.get('linkedin_url')
            facebook_url = self.request.get('facebook_url')
            twitter_handle = self.request.get('twitter_handle')
            skype_id = self.request.get('skype_id')
            blog_url = self.request.get('blog_url')
            gravatar_url = get_gravatar_url(160,user.email)
            profileinfo = {'first_name': first_name,
                           'last_name': last_name,
                           'gravatar_url':gravatar_url,
                           'country': country,
                           'city': city,
                           'linkedin_url': linkedin_url,
                           'facebook_url': facebook_url,
                           'twitter_handle': twitter_handle,
                           'skype_id': skype_id,
                           'blog_url': blog_url}
            profile = UserThinDB.all().filter('user_name = ', user.user_name).filter('asset =','profile').filter('asset_key =','info').get()
            if profile:
                profile.str_value = json.dumps(profileinfo)
                profile.put()
            else:
                profile = UserThinDB(user_name=user.user_name, asset='profile',asset_key='info', str_value=json.dumps(profileinfo), int_value=0)
                profile.put()
            self.redirect('/home/'+user.user_name)

        else:
            self.redirect('/signin')


class UserInternalProfileHandler(SLRequestHandler):
    @login_required
    def get(self, username):
        profile = UserThinDB.all().filter('user_name = ', username).filter('asset =','profile').filter('asset_key =','info').get()
        if profile:
            variables = json.loads(profile.str_value)
            template = jinja_environment.get_template('userinternalindex.html')
            self.response.out.write(template.render(variables))
        else:
            self.response.out.write('no such user profile exists!')


class UserExternalProfileHandler(SLRequestHandler):
    def get(self, user_name):
        profile = UserThinDB.all().filter('user_name = ', user_name).filter('asset =','profile').filter('asset_key =','info').get()
        if profile:
            variables = json.loads(profile.str_value)
            template = jinja_environment.get_template('userexternalindex.html')
            self.response.out.write(template.render(variables))
        else:
            self.response.out.write('no such user profile exists!')


class UserPrivateProfileHandler(SLRequestHandler):
    @login_required
    def get(self, user_name):
        #Need check that user making request is the same as the user_name - if not redirect to their profile page
        profile = UserThinDB.all().filter('user_name = ', user_name).filter('asset =','profile').filter('asset_key =','info').get()
        if profile:
            variables = json.loads(profile.str_value)
            template = jinja_environment.get_template('userprivateindex.html')
            self.response.out.write(template.render(variables))
        else:
            self.response.out.write('no such user profile exists!')


class UserEditProfileHandler(SLRequestHandler):
    @login_required
    def get(self, user_name):
        #Need check that user making request is the same as the user_name - if not redirect to their profile page
        profile = UserThinDB.all().filter('user_name = ', user_name).filter('asset =','profile').filter('asset_key =','info').get()
        if profile:
            variables = json.loads(profile.str_value)
            template = jinja_environment.get_template('userprofileedit.html')
            self.response.out.write(template.render(variables))
        else:
            self.response.out.write('no such user profile exists!')

    @login_required
    def post(self, username):
        if self.is_logged_in():
            user = self.user
            first_name = self.request.get('first_name')
            last_name = self.request.get('last_name')
            country = self.request.get('country')
            city = self.request.get('city')
            linkedin_url = self.request.get('linkedin_url')
            facebook_url = self.request.get('facebook_url')
            twitter_handle = self.request.get('twitter_handle')
            skype_id = self.request.get('skype_id')
            blog_url = self.request.get('blog_url')
            description = self.request.get('description')
            profileinfo = {'first_name': first_name, 'last_name': last_name, 'country': country, 'city': city, 'linkedin_url': linkedin_url, 'facebook_url': facebook_url, 'twitter_handle': twitter_handle, 'skype_id': skype_id, 'blog_url': blog_url, 'description': description}
            profile = UserThinDB.all().filter('user_name = ', user.user_name).filter('asset =','profile').filter('asset_key =','info').get()
            if profile:
                profile.str_value = json.dumps(profileinfo)
                profile.put()
            else:
                profile = UserThinDB(user_name=user.user_name, asset='profile',asset_key='info', str_value=json.dumps(profileinfo), int_value=0)
                profile.put()
            self.redirect('/user/profile/'+user.user_name)

        else:
            self.redirect('/signin')

class SignUpHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('signup.html')
        variables = {}
        self.response.out.write(template.render(variables))

    def post(self):
        email = self.request.get('email')
        username = self.request.get('username')
        password = self.request.get('password')
        username_exists = User.all().filter('user_name =', username).get()
        if not username_exists:
            #save the new user unactivated
            random_secret = "".join(random.choice(string.letters) for x in xrange(5))
            password_hash = random_secret+'|'+hmac.new(random_secret,password).hexdigest()
            activation_key = hmac.new(random_secret,username).hexdigest()
            new_user = User(email=email, user_name=username, password_hash=password_hash, activated='False', activation_key=activation_key)
            new_user.put()
            #mail the activation link
            activation_link = domain+'/account_activation?activation_key='+hmac.new(random_secret,username).hexdigest()
            email_template = jinja_environment.get_template('email.html')
            try:
                mail.send_mail(sender="ServeLife <alan@servelife.com>",
                                to=email,
                                subject="Activate your Servelife account!",
                                body="no html version",
                                html=email_template.render({'activation_link':activation_link}))
            except:
                self.response.out.write('mail config not working..')

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
            username = user.username
            user_influence = UserThinDB(user_name=username,
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

                #ABR: check to see if the user has a profile
                profile = UserThinDB.all().filter('user_name = ', user.user_name).filter('asset =', 'profile').filter('asset_key =', 'info').get()
                if profile:
                    self.redirect('/home/'+user.user_name)
                else:
                    self.redirect('/userprofile/new/'+user.user_name)
            else:
                self.response.out.write('password error!')
        else:
            self.response.out.write('no such email signup with us!')


class LogOutHandler(SLRequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie','user_id=;Path = /')
        self.redirect('/')


class UserHomePageHandler(SLRequestHandler):
    @login_required
    def get(self, username):
        template = jinja_environment.get_template('userhome.html')
        variables = {}
        self.response.out.write(template.render(variables))


class KnowledgeCenterPageHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('discover.html')
        variables = {}
        self.response.out.write(template.render(variables))


class LearningCenterPageHandler(SLRequestHandler):
    def get(self):
        template = jinja_environment.get_template('learn.html')
        variables = {}
        self.response.out.write(template.render(variables))


class NewCourseProfileHandler(SLRequestHandler):
    @login_required
    def get(self):
        template = jinja_environment.get_template('newcourseprofile.html')
        user_name = self.user.user_name
        variables = {user_name}
        self.response.out.write(template.render(variables))

    @login_required
    def post(self):
        user = self.user
        course_name = self.request.get('course_name')
        course_url = self.request.get('course_url')
        courseinfo = {'course_name': course_name, 'course_url': course_url}
        course = CourseThinDB.all().filter('course_name = ', course_name).filter('asset =', 'profile').filter('asset_key =','info').get()
        if course:
            course.str_value = json.dumps(courseinfo)
            course.put()
        else:
            course = CourseThinDB(course_name=course_name, asset='profile', asset_key='info', str_value=json.dumps(courseinfo), int_value=0, created_by=user)
            course.put()
        self.redirect('/course/'+course_name)


class ShowCourseHandler(SLRequestHandler):
    def get(self, course_name):
        template = jinja_environment.get_template('courseindex.html')
        variables = {}
        self.response.out.write(template.render(variables))


class NewTopicProfileHandler(SLRequestHandler):
    @login_required
    def get(self):
        template = jinja_environment.get_template('newcourseprofile.html')
        user_name = self.user.user_name
        variables = {user_name}
        self.response.out.write(template.render(variables))

    @login_required
    def post(self):
        user = self.user
        course_name = self.request.get('course_name')
        course_url = self.request.get('course_url')
        courseinfo = {'course_name': course_name, 'course_url': course_url}
        course = CourseThinDB.all().filter('course_name = ', course_name).filter('asset =', 'profile').filter('asset_key =','info').get()
        if course:
            course.str_value = json.dumps(courseinfo)
            course.put()
        else:
            course = CourseThinDB(course_name=course_name, asset='profile', asset_key='info', str_value=json.dumps(courseinfo), int_value=0, created_by=user)
            course.put()
        self.redirect('/course/'+course_name)


class ShowTopicHandler(SLRequestHandler):
    def get(self, course_name):
        template = jinja_environment.get_template('courseindex.html')
        variables = {}
        self.response.out.write(template.render(variables))


#ABR not used yet - moved to clean up
# class TeamProfileHandler(SLRequestHandler):
#     def get(self):
#         template = jinja_environment.get_template('teampublicprofile.html')
#         variables = {}
#         self.response.out.write(template.render(variables))
#
#
# class ProjectProfileHandler(SLRequestHandler):
#     def get(self):
#         template = jinja_environment.get_template('projectpublicprofile.html')
#         variables = {}
#         self.response.out.write(template.render(variables))
#
#
# class ProjectCenterPageHandler(SLRequestHandler):
#     def get(self):
#         template = jinja_environment.get_template('learn.html')
#         variables = {}
#         self.response.out.write(template.render(variables))
#
#
# class ClassProfilePageHandler(SLRequestHandler):
#     def get(self):
#         template = jinja_environment.get_template('class.html')
#         variables = {}
#         self.response.out.write(template.render(variables))
#
#
# class CourseProfilePageHandler(SLRequestHandler):
#     def get(self):
#         template = jinja_environment.get_template('course.html')
#         variables = {}
#         self.response.out.write(template.render(variables))
#
#
# @login_required
# class GetUserFeedHandler(SLRequestHandler):
#     def get(self, username):
#         user = 'mogambo'
#         if self.is_logged_in():
#             user = self.user
#             self.response.out.write('feed from username: '+username+'. Logged in user is:'+user.username)
#
# class GetUserTopicFeedHandler(SLRequestHandler):
#     @login_required
#     def get(self, username, topic):
#         self.response.out.write('feed from username: '+username+' on topic: '+topic)
#
# class AddCourseHandler(SLRequestHandler):
#     @login_required
#     def get(self):
#         #add course form
#         pass


app = webapp2.WSGIApplication([('/', LandingPageHandler),
                               ('/innovationintheenterprise', PodcastHandler),
                               ('/userprofile/new/(?P<username>.*)', UserProfileNewHandler),
                               ('/profile/(?P<username>.*)', UserInternalProfileHandler),
                               ('/member/(?P<user_name>.*)', UserExternalProfileHandler),
                               ('/user/profile/edit/(?P<user_name>.*)', UserEditProfileHandler),
                               ('/user/profile/(?P<user_name>.*)', UserPrivateProfileHandler),
                               #('/user/account/(?P<user_name>.*)', UserAccountHandler),
                               #('/teamprofile/(?P<team>.*)', TeamProfileHandler),
                               #('/projectprofile/(?P<project>.*)', ProjectProfileHandler),
                               ('/signup', SignUpHandler),
                               ('/account_activation', ActivationHandler),
                               ('/signin', SignInHandler),
                               ('/logout', LogOutHandler),
                               #('/get_user_feed/(?P<username>.*)', GetUserFeedHandler),
                               #('/get_user_feed_by_topic/(?P<username>.*)/(?P<topic>.*)', GetUserTopicFeedHandler),
                               #('/add_a_course', AddCourseHandler),
                               ('/home/(?P<username>.*)', UserHomePageHandler),
                               #('/course', CourseProfilePageHandler),
                               #('/class', ClassProfilePageHandler),
                               ('/discover', KnowledgeCenterPageHandler),
                               ('/learn', LearningCenterPageHandler),
                               #('/project', ProjectCenterPageHandler),
                                ('/course/new', NewCourseProfileHandler),
                                ('/course/(?P<course_name>.*)', ShowCourseHandler)
                               ],
                              debug=True)
