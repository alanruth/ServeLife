import os
import random
import string
import hmac
import json
import urllib
import hashlib
import logging


import webapp2
import jinja2
from google.appengine.api import mail
from google.appengine.api import search
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from models.models import *


#'http://localhost:8080'
domain = 'http://learnmastermentor.appspot.com'

jinja_environment = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'views')))

def create_topic(topic):
    topic_info = json.loads(topic.str_value)
    topic_description = topic_info.get('topic_description')
    parent_topic = topic_info.get('parent_topic')
    created_by = topic.created_by.user_name
    return search.Document(doc_id=str(topic.key().id()),fields = [search.TextField(name='description',value=topic_description),
                                                                 search.TextField(name='parent_topic', value=parent_topic),
                                                                 search.TextField(name='created_by', value=created_by),])


#utility function to get gravatar image url
def get_gravatar_url(size, email):
    default = domain + "/static/img/defaultavatar.png"
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url

jinja_environment.filters['get_gravatar_url'] = get_gravatar_url

#decorator for protecting pages
def login_required(function):
    def _f(self, *args, **kwargs):
        if self.is_logged_in():
            function(self, *args, **kwargs)
        else:
            next_page = self.request.path
            self.redirect('/signin?next=%s' %next_page)

    return _f


#function to increment follower & follow counts for a user (how many people follow the user and how many they follow)
def user_follow(user_followed, user_follower):
    user_followed.follower_count += 1
    user_followed.put()
    user_follower.follow_count += 1
    user_follower.put()

    return True


def user_unfollow(user_unfollowed, user_follower):
    user_unfollowed.follower_count -= 1
    user_unfollowed.put()
    user_follower.follow_count -= 1
    user_follower.put()

    return True


#function to increment follower & follow counts for a user (how many people follow the user and how many they follow)
def topic_follow(topic_followed, user_follower):
    topic_followed.follower_count += 1
    topic_followed.put()
    user_follower.topics_followed += 1
    user_follower.put()

    return True


def course_follow(course_followed, user_follower):
    course_followed.follower_count += 1
    course_followed.put()
    user_follower.courses_followed += 1
    user_follower.put()

    return True





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

class SLBSRequestHandler(SLRequestHandler, blobstore_handlers.BlobstoreUploadHandler):
    pass

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
    def get(self, user_name):
        if self.is_logged_in():
            user = self.user
            #profileinfo is a json string with keys name, title and about
            profile = UserThinDB.all().filter('user_name = ', user.user_name).filter('asset =', 'profile').filter('asset_key =', 'info').get()
            profileinfo='{}'
            if profile:
                profileinfo=profile.str_value


            """
            variables = {'name': name,
                         'title': title,
                         'about':about}
            """

            variables = json.loads(profileinfo)
            variables['userthin'] = profile
            template = jinja_environment.get_template('newuserprofile.html')
            self.response.out.write(template.render(variables))
        else:
            self.redirect('/signin')

    @login_required
    def post(self, user_name):
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
            gravatar_url = get_gravatar_url(180, user.email)
            profileinfo = {'first_name': first_name,
                           'last_name': last_name,
                           'country': country,
                           'city': city,
                           'linkedin_url': linkedin_url,
                           'facebook_url': facebook_url,
                           'twitter_handle': twitter_handle,
                           'skype_id': skype_id,
                           'gravatar_url': gravatar_url}
            profile = UserThinDB.all().filter('user_name = ', user.user_name).filter('asset =','profile').filter('asset_key =','info').get()
            if profile:
                profile.str_value = json.dumps(profileinfo)
                profile.put()
            else:
                profile = UserThinDB(user_name=user.user_name, asset='profile',asset_key='info', str_value=json.dumps(profileinfo), int_value=0)
                profile.put()
            self.redirect('/home/hub/' + user.user_name)

        else:
            self.redirect('/signin')


class UserInternalProfileHandler(SLRequestHandler):
    @login_required
    def get(self, user_name):
        if self.is_logged_in():
            profile = UserThinDB.all().filter('user_name = ', user_name).filter('asset =','profile').filter('asset_key =','info').get()
            if profile:
                variables = json.loads(profile.str_value)
                variables['userthin'] = profile
                variables['user_email'] = self.user.email
                template = jinja_environment.get_template('userinternalindex.html')
                self.response.out.write(template.render(variables))
            else:
                self.response.out.write('no such user profile exists!')

        else:
            self.redirect('/signin')


class UserExternalProfileHandler(SLRequestHandler):
    def get(self, user_name):
        profile = UserThinDB.all().filter('user_name = ', user_name).filter('asset =','profile').filter('asset_key =','info').get()
        if profile:
            variables = json.loads(profile.str_value)
            variables['userthin'] = profile
            template = jinja_environment.get_template('userexternalindex.html')
            self.response.out.write(template.render(variables))
        else:
            self.response.out.write('no such ServeLife member exists within the ecosystem!')


class TopicExternalProfileHandler(SLRequestHandler):
    def get(self, topic_name):
        topic = TopicThinDB.all().filter('topic_name = ', topic_name).filter('asset =','profile').filter('asset_key =','info').get()
        if topic:
            variables = json.loads(topic.str_value)
            variables['topic'] = topic
            template = jinja_environment.get_template('topicexternalindex.html')
            self.response.out.write(template.render(variables))
        else:
            self.response.out.write('no such topic exists within the ServeLife ecosystem!')


class ProjectExternalProfileHandler(SLRequestHandler):
    def get(self, project_name):
        project = ProjectThinDB.all().filter('project_name = ', project_name).filter('asset =','profile').filter('asset_key =','info').get()
        if project:
            variables = json.loads(project.str_value)
            template = jinja_environment.get_template('projectexternalindex.html')
            self.response.out.write(template.render(variables))
        else:
            self.response.out.write('no such project exists within the ServeLife ecosystem!')


class UserPrivateProfileHandler(SLRequestHandler):
    @login_required
    def get(self, user_name):
        if self.is_logged_in():
            user = self.user
            profile = UserThinDB.all().filter('user_name = ', user.user_name).filter('asset =','profile').filter('asset_key =','info').get()
            if profile:
                variables = json.loads(profile.str_value)
                template = jinja_environment.get_template('userprivateindex.html')
                self.response.out.write(template.render(variables))
            else:
                self.response.out.write('no such user profile exists!')


class UserProfileEditHandler(SLRequestHandler):
    @login_required
    def get(self, user_name):
        if self.is_logged_in():
            user = self.user
            profile = UserThinDB.all().filter('user_name = ', user.user_name).filter('asset =','profile').filter('asset_key =','info').get()
            if profile:
                variables = json.loads(profile.str_value)
                variables['userthin'] = profile
                variables['user_email'] = self.user.email
                template = jinja_environment.get_template('userprofileedit.html')
                self.response.out.write(template.render(variables))
            else:
                self.response.out.write('no such user profile exists!')

        else:
            self.redirect('/signin')


    @login_required
    def post(self, user_name):
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
            description = self.request.get('description')
            gravatar_url = get_gravatar_url(180, user.email)
             #avatar = images.resize(self.request.get('img'), 180, 180)
            profileinfo = {
                'first_name': first_name,
                'last_name': last_name,
                'country': country,
                'city': city,
                'linkedin_url': linkedin_url,
                'facebook_url': facebook_url,
                'twitter_handle': twitter_handle,
                'skype_id': skype_id,
                'description': description,
                'gravatar_url': gravatar_url}
            profile = UserThinDB.all().filter('user_name = ', user.user_name).filter('asset =','profile').filter('asset_key =','info').get()
            if profile:
                profile.str_value = json.dumps(profileinfo)
                #profile.profile_pic = avatar
                profile.put()
            else:
                profile = UserThinDB(user_name=user.user_name,
                                     asset='profile',
                                     asset_key='info',
                                     str_value=json.dumps(profileinfo),
                                     int_value=0)
                profile.put()
            self.redirect('/profile/user/' + user.user_name)

        else:
            self.redirect('/signin')


class UserAccountEditHandler(SLRequestHandler):
    @login_required
    def get(self, user_name):
        if self.is_logged_in():
            user = self.user
            account = User.all().filter('user_name = ', user.user_name).get()
            if account:
                variables = {'user_name': user.user_name, 'user_email': user.email}
                template = jinja_environment.get_template('useraccountedit.html')
                self.response.out.write(template.render(variables))
            else:
                self.response.out.write('no such user account exists!')

        else:
            self.redirect('/signin')


class UserSubscriptionEditHandler(SLRequestHandler):
    @login_required
    def get(self, user_name):
        if self.is_logged_in():
            user = self.user
            account = User.all().filter('user_name = ', user.user_name).get()
            if account:
                variables = {'user_name': user.user_name, 'user_email': user.email}
                template = jinja_environment.get_template('usersubscriptionedit.html')
                self.response.out.write(template.render(variables))
            else:
                self.response.out.write('no such user subscription exists!')

        else:
            self.redirect('/signin')


class SignUpHandler(SLRequestHandler):
    def get(self):
        if self.is_logged_in():
            user = self.user
            self.redirect('/home/'+user.user_name)
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
        if self.is_logged_in():
            user = self.user
            self.redirect('/home/hub/'+user.user_name)
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
                    self.redirect('/home/hub/'+user.user_name)
                else:
                    self.redirect('/user/profile/new/' + user.user_name)
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
    def get(self, user_name):
        if self.is_logged_in():
            user = self.user
            template = jinja_environment.get_template('userhome.html')
            variables = {'user': user, 'user_name': user.user_name, 'user_email': user.email}
            self.response.out.write(template.render(variables))


class DiscoverHubIndexHandler(SLRequestHandler):
    @login_required
    def get(self):
        if self.is_logged_in():
            user = self.user
            template = jinja_environment.get_template('discover.html')
            variables = {'user': user, 'user_email': user.email, 'user_name': user.user_name}
            self.response.out.write(template.render(variables))

        else:
            self.redirect('/signin')


class LearningCenterPageHandler(SLRequestHandler):
    @login_required
    def get(self, user_name):
        if self.is_logged_in():
            user = self.user
            template = jinja_environment.get_template('learnprivateindex.html')
            variables = {'user': user, 'user_email': user.email, 'user_name': user.user_name}
            self.response.out.write(template.render(variables))

        else:
            self.redirect('/signin')


class NewCourseProfileHandler(SLRequestHandler):
    @login_required
    def get(self):
        if self.is_logged_in():
            variables = {'user_email': self.user.email}
            template = jinja_environment.get_template('newcourseprofile.html')
            self.response.out.write(template.render(variables))

        else:
            self.redirect('/signin')

    @login_required
    def post(self):
        user = self.user
        course_name = self.request.get('course_name')
        course_url = self.request.get('course_url')
        course_tags = self.request.get('course_tags').split(',')
        course_organization = self.request.get('organization_name')
        free = self.request.get('course_free')
        courseinfo = {'course_name': course_name, 'course_url': course_url, 'course_organization': course_organization, 'course_free': free}
        course = CourseThinDB.all().filter('course_name = ', course_name.lower()).filter('asset =', 'profile').filter('asset_key =','info').get()
        if course:
            course.course_tags = course_tags
            course.str_value = json.dumps(courseinfo)
            course.put()
        else:
            course = CourseThinDB(course_name=course_name, asset='profile', asset_key='info', str_value=json.dumps(courseinfo), int_value=0, created_by=user, course_tags=course_tags)
            course.put()
        self.redirect('/course/'+course_name)


class CourseEditProfileHandler(SLRequestHandler):
    @login_required
    def get(self, course_name):
        if self.is_logged_in():
            course_name = course_name.lower()
            course = CourseThinDB.all().filter('course_name = ', course_name).filter('asset =','profile').filter('asset_key =','info').get()
            if course:
                #self.response.out.write(course_name)
                variables = json.loads(course.str_value)
                tags = ", ".join(course.course_tags)
                variables['course_tags'] = tags
                variables['user_email'] = self.user.email
                template = jinja_environment.get_template('courseprofileedit.html')
                self.response.out.write(template.render(variables))
            else:
                self.response.out.write('no such course exists.')

        else:
            self.redirect('/signin')

    @login_required
    def post(self, course_name):
        course_name = self.request.get('course_name').lower
        course_url = self.request.get('course_url')
        course_tags = self.request.get('course_tags').split(',')
        course_organization = self.request.get('organization_name')
        free = self.request.get('course_free')
        courseinfo = {'course_name': course_name, 'course_url': course_url, 'course_organization': course_organization, 'course_free': free}
        course = CourseThinDB.all().filter('course_name = ', course_name).filter('asset =', 'profile').filter('asset_key =', 'info').get()
        if course:
            course.course_tags = course_tags
            course.str_value = json.dumps(courseinfo)
            course.put()
        else:
            course = CourseThinDB(course_name=course_name, asset='profile', asset_key='info', str_value=json.dumps(courseinfo), int_value=0, created_by=user, course_tags=course_tags)
            course.put()
        self.redirect('/course/'+course_name)


class CourseInternalIndexHandler(SLRequestHandler):
    @login_required
    def get(self, course_name):
        if self.is_logged_in():
            course = CourseThinDB.all().filter('course_name = ', course_name).filter('asset =', 'profile').filter('asset_key =', 'info').get()
            if course:
                template = jinja_environment.get_template('courseinternalindex.html')
                variables = json.loads(course.str_value)
                variables['course'] = course
                variables['user_email'] = self.user.email
                self.response.out.write(template.render(variables))
            else:
                self.response.out.write('no such course exists.')

        else:
            self.redirect('/signin')


class TopicInternalIndexHandler(SLRequestHandler):
    @login_required
    def get(self, topic_name):
        if self.is_logged_in():
            topic = TopicThinDB.all().filter('topic_name = ', topic_name).filter('asset =', 'profile').filter('asset_key =', 'info').get()
            if topic:
                template = jinja_environment.get_template('topicinternalindex.html')
                variables = json.loads(topic.str_value)
                variables['topic'] = topic
                variables['user_email'] = self.user.email
                variables['user_name'] = self.user.user_name
                variables['blob_key'] = json.loads(topic.str_value).get('blob_key')
                self.response.out.write(template.render(variables))

            else:
                self.response.out.write('no such topic exists.')

        else:
            self.redirect('/signin')


class DiscoverTopicIndexHandler(SLRequestHandler):
    @login_required
    def get(self):
        if self.is_logged_in():
            user = UserThinDB.all().filter('user_name = ', self.user.user_name).get()
            topics = []
            topics_followed = db.GqlQuery(
                "SELECT __key__ FROM TopicFollowerIndex WHERE followers = :1", user.key().id())
            topics.extend(db.get([k.parent() for k in topics_followed]))
            template = jinja_environment.get_template('topicprivateindex.html')
            variables = {'user_email': self.user.email, 'user_name': self.user.user_name, 'topics': topics}
            self.response.out.write(template.render(variables))
        else:
            self.redirect('/signin')


class NewTopicProfileHandler(SLBSRequestHandler):
    @login_required
    def get(self):
        if self.is_logged_in():
            upload_url = blobstore.create_upload_url('/topic/new')
            #upload_url = blobstore.create_upload_url('/upload')
            template = jinja_environment.get_template('topicnewprofile.html')
            variables = {'user_email': self.user.email,'upload_url':upload_url}
            self.response.out.write(template.render(variables))

        else:
            self.redirect('/signin')

    @login_required
    def post(self):
        if self.is_logged_in():
            user = self.user
            topic_name = self.request.get('topic_name')
            topic_name_lc = topic_name.lower()
            topic_description = self.request.get('topic_description')
            parent_topic = self.request.get('parent_topic')
            upload_files = self.get_uploads('topic_image')
            blob_info = upload_files[0]
            topicinfo = {'topic_name': topic_name,
                         'topic_description': topic_description,
                         'parent_topic': parent_topic,
                         'blob_key':str(blob_info.key()),
                        }
            topic = TopicThinDB.all().filter('topic_name = ', topic_name_lc).filter('asset =', 'profile').filter('asset_key =','info').get()
            if topic:
                topic.created_by = user
                topic.updater = user
                topic.str_value = json.dumps(topicinfo)
                topic.put()
            else:
                topic = TopicThinDB(topic_name=topic_name_lc, asset='profile', asset_key='info', str_value=json.dumps(topicinfo), int_value=0, created_by=user, updater=user)
                topic.updater = user
                topic.put()
            doc = create_topic(topic)
            _INDEX_NAME = 'topic'
            try:
                search.Index(name=_INDEX_NAME).put(doc)
                self.redirect('/discover/topic/'+topic_name_lc)
            except search.Error:
                logging.exception('Add failed')


        else:
            self.redirect('/signin')


class FollowUserHandler(SLRequestHandler):
    @login_required
    def post(self, followed):
        if self.is_logged_in():
            #user that is following another user is the follower
            user_follower = UserThinDB.all().filter('user_name = ', self.user.user_name).get()
            #user that is being followed is the followed
            user_followed = UserThinDB.all().filter('user_name = ', followed).get()
            follow_index = UserFollowerIndex.all().filter('parent = ', user_followed).get()
            if follow_index:
                follow_index = UserFollowerIndex.followers.append(user_follower.key().id())
                follow_index.put()
            else:
                follow_index = UserFollowerIndex(key_name='index', parent=user_followed, followers=[(user_follower.key().id())])
                follow_index.put()

            #Increment how many users follow a a certain user = follower count and
            #Increment how many users a certain user follows = follow count
            user_follow(user_followed, user_follower)
            self.redirect('/user/profile/' + followed)
        else:
            self.redirect('/signin')


class FollowTopicHandler(SLRequestHandler):
    @login_required
    def post(self, topic):
        if self.is_logged_in():
            follower = UserThinDB.all().filter('user_name = ', self.user.user_name).get()
            topic_followed = TopicThinDB.all().filter('topic_name = ', topic).get()
            follow_index = TopicFollowerIndex.all().filter('parent = ', topic_followed).get()
            if follow_index:
                follow_index = TopicFollowerIndex.followers.append((follower.key().id()))
                follow_index.put()
            else:
                follow_index = TopicFollowerIndex(key_name='index', parent=topic_followed, followers=[(follower.key().id())])
                follow_index.put()

            #Increment how many users follow a a certain user = follower count and
            #Increment how many users a certain user follows = follow count
            topic_follow(topic_followed, follower)
            self.redirect('/discover/topic/'+topic)
        else:
            self.redirect('/signin')


class FollowCourseHandler(SLRequestHandler):
    @login_required
    def post(self, course_name):
        if self.is_logged_in():
            #user that is following course
            user_follower = UserThinDB.all().filter('user_name = ', self.user.user_name).get()
            course_followed = CourseThinDB.all().filter('course_name = ', course_name).get()
            follow_index = CourseFollowerIndex.all().filter('parent = ', course_followed).get()
            if follow_index:
                follow_index = CourseFollowerIndex.followers.append(user_follower.key().id())
                follow_index.put()
            else:
                follow_index = CourseFollowerIndex(key_name='index', parent=course_followed, followers=[(user_follower.key().id())])
                follow_index.put()

            #Increment how many users follow a a certain user = follower count and
            #Increment how many users a certain user follows = follow count
            user_follow(course_followed, user_follower)
            self.redirect('/course/'+course_name)
        else:
            self.redirect('/signin')


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
#         template = jinja_environment.get_template('learnprivateindex.html')
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


def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

class SearchHandler(webapp2.RequestHandler):
    def get(self, index):
        q = self.request.get('q')
        _INDEX_NAME = index
        try:
            results = search.Index(name=_INDEX_NAME).search(q)
            template = jinja_environment.get_template('results.html')
            variables = {'results':results,'query':q}
            self.response.out.write(template.render(variables))
        except search.Error:
            logging.exception('search failed')


class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)


app = webapp2.WSGIApplication([
                                  (r'/', LandingPageHandler),
                                  ('/innovationintheenterprise', PodcastHandler),
                                  ('/member/profile/(?P<user_name>.*)', UserExternalProfileHandler),
                                  ('/topic/profile/(?P<topic_name>.*)', TopicExternalProfileHandler),
                                  ('/project/profile/(?P<project_name>.*)', ProjectExternalProfileHandler),
                                  ('/signup', SignUpHandler),
                                  ('/account_activation', ActivationHandler),
                                  ('/signin', SignInHandler),
                                  ('/logout', LogOutHandler),
                                  ('/user/profile/new/(?P<username>.*)', UserProfileNewHandler),
                                  ('/user/profile/(?P<user_name>.*)', UserProfileEditHandler),
                                  ('/user/account/(?P<user_name>.*)', UserAccountEditHandler),
                                  ('/user/subscription/(?P<user_name>.*)', UserSubscriptionEditHandler),
                                  ('/profile/(?P<user_name>.*)', UserPrivateProfileHandler),
                                  ('/user/profile/(?P<user_name>.*)', UserInternalProfileHandler),
                                  ('/home/hub/(?P<user_name>.*)', UserHomePageHandler),
                                  #('/home/contributions/(?P<user_name>.*)', UserContributionsPageHandler),
                                  #('/home/achievements/(?P<user_name>.*)', UserAchievementsPageHandler),
                                  #('/home/efforts/(?P<user_name>.*)', UserEffortsPageHandler),
                                  #('/home/tribe/(?P<user_name>.*)', UserTribePageHandler),
                                  ('/topic/new', NewTopicProfileHandler),
                                  ('/discover/topic/(?P<topic_name>.*)', TopicInternalIndexHandler),
                                  ('/discover/topics.*', DiscoverTopicIndexHandler),
                                  ('/discover/hub.*', DiscoverHubIndexHandler),
                                  ('/learn/hub/(?P<user_name>.*)', LearningCenterPageHandler),
                                  ('/course/new', NewCourseProfileHandler),
                                  ('/course/edit/(?P<course_name>.*)', CourseEditProfileHandler),
                                  ('/course/(?P<course_name>.*)', CourseInternalIndexHandler),
                                  ('/follow/(?P<followed>.*)', FollowUserHandler),
                                  ('/followcourse/(?P<followed>.*)', FollowCourseHandler),
                                  ('/followtopic/(?P<followed>.*)', FollowTopicHandler),
                                  ('/search/(?P<index>.*)', SearchHandler),
                                  ('/serve/([^/]+)?', ServeHandler),
                                  #('/project', ProjectCenterPageHandler),
                                  #('/user/account/(?P<user_name>.*)', UserAccountHandler),
                                  #('/teamprofile/(?P<team>.*)', TeamProfileHandler),
                                  #('/projectprofile/(?P<project>.*)', ProjectProfileHandler),
                                  #('/get_user_feed/(?P<username>.*)', GetUserFeedHandler),
                                  #('/get_user_feed_by_topic/(?P<username>.*)/(?P<topic>.*)', GetUserTopicFeedHandler),
                                  #('/add_a_course', AddCourseHandler),
                                  #('/course', CourseProfilePageHandler),
                                  #('/class', ClassProfilePageHandler),
                              ],
                              debug=True)

app.error_handlers[404] = handle_404
