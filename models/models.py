from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.ext.db import polymodel


class Subscriber(db.Model):
    email = db.StringProperty(required=True)
    created = db.DateTimeProperty(required=True,auto_now_add=True)
    verified = db.BooleanProperty(required=True)


class UserCount(ndb.Model):
    entity_type = ndb.StringProperty(required=True)
    count = ndb.IntegerProperty(required=True)


class UserGoal(ndb.Model):
    user = ndb.KeyProperty(kind='User')
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=False)
    rank = ndb.IntegerProperty(required=False, default=0)
    goal_status = ndb.StringProperty(choices=('completed', 'active', 'not started', 'on hold', 'deleted'))
    accomplished_measure = ndb.StringProperty(required=False)
    due_date = ndb.DateProperty(required=False)
    started_date = ndb.DateTimeProperty(required=False)
    completed_date = ndb.DateTimeProperty(required=False)
    completed_comment = ndb.StringProperty(required=False)
    tags = ndb.JsonProperty()
    private = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(required=True, auto_now_add=True)
    updated = ndb.DateTimeProperty(required=True, auto_now=True)


class User(ndb.Model):
    user_name           = ndb.StringProperty(required=True)
    password_hash       = ndb.StringProperty(required=True)
    email               = ndb.StringProperty(required=True)
    activated           = ndb.StringProperty(required=True)
    activation_key      = ndb.StringProperty(required=True)
    created             = ndb.DateTimeProperty(required=True, auto_now_add=True)
    profile             = ndb.JsonProperty(indexed=True)
    goals               = ndb.StructuredProperty(UserGoal, repeated=True)
    following           = ndb.StructuredProperty(UserCount, repeated=True)
    locked              = ndb.BooleanProperty()


class GoalAction(UserGoal):
    estimate = ndb.IntegerProperty(default=0)
    effort_to_date = ndb.IntegerProperty(default=0)
    effort_remaining = ndb.IntegerProperty()
    progress = ndb.FloatProperty()


class UserGoalEvent(ndb.Model):
    goal = ndb.KeyProperty(kind='UserGoal')
    event = ndb.StringProperty(required=True)
    reason = ndb.StringProperty(required=False)
    created = ndb.DateTimeProperty(required=True, auto_now_add=True)


class TeamMember(ndb.Model):
    member = ndb.KeyProperty(kind='User')
    role = ndb.StringProperty(required=False)
    joined = ndb.DateTimeProperty(required=True, auto_now_add=True)
    active = ndb.BooleanProperty(default=True)
    inactivated = ndb.DateTimeProperty(required=False)
    admin = ndb.BooleanProperty(default=False)


class TeamOpening(ndb.Model):
    role                = ndb.StringProperty(required=True)
    description         = ndb.StringProperty(required=True)
    skills              = ndb.JsonProperty()
    commitment_sought   = ndb.StringProperty()
    created             = ndb.DateTimeProperty(required=True, auto_now_add=True)
    posted              = ndb.DateTimeProperty()
    closed              = ndb.DateTimeProperty()
    filled              = ndb.BooleanProperty()
    filled_with         = ndb.KeyProperty(kind='User')
    revision            = ndb.IntegerProperty()


class Project(ndb.Model):
    project_name        = ndb.StringProperty(required= True)
    profile             = ndb.JsonProperty()
    follower_count      = ndb.IntegerProperty(required=False, default=0)
    created             = ndb.DateTimeProperty(required=True, auto_now_add=True)
    created_by          = ndb.KeyProperty(kind='User')
    start_date          = ndb.DateProperty(required=True)
    team_members        = ndb.StructuredProperty(TeamMember, repeated=True)
    team_openings       = ndb.StructuredProperty(TeamOpening, repeated=True)
    tags                = ndb.JsonProperty()


class Question(ndb.Model):
    entity_object       = ndb.KeyProperty()
    entity_type         = ndb.StringProperty()
    subject             = ndb.StringProperty()
    body                = ndb.TextProperty()
    created             = ndb.DateTimeProperty(required=True, auto_now_add=True)
    owner               = ndb.KeyProperty(kind='User')
    question_type       = ndb.StringProperty()
    active              = ndb.BooleanProperty()
    tags                = ndb.JsonProperty()


#class UserThinDB(ndb.Model):
#    user_name      = ndb.StringProperty(required=True)
#    asset         = ndb.StringProperty(required=True)
#    asset_key     = ndb.StringProperty(required=True)
#    str_value     = ndb.StringProperty(required=False)
#    int_value     = ndb.IntegerProperty(required=False)
#    follower_count = ndb.IntegerProperty(required=False, default=0)
#    follow_count = ndb.IntegerProperty(required=False, default=0)
#    topics_followed = ndb.IntegerProperty(required=False, default=0)
#    courses_followed = ndb.IntegerProperty(required=False, default=0)
#    projects_followed = ndb.IntegerProperty(required=False, default=0)
#    created       = ndb.DateTimeProperty(required=True, auto_now_add=True)
#    updated       = ndb.DateTimeProperty(required=True, auto_now=True)
#    profile_pic     = ndb.StringProperty()
#    active_goals = ndb.IntegerProperty(default=0)
#    goals = ndb.StructuredProperty(UserGoal, repeated=True)

    #def set_active_goals(self):
    #    self.active_goals = self.calculate_active_goals()

    #def calculate_active_goals(self):
    #    goals = UserGoal.all().filter('goal_user = ', self).count(25)
    #    if goals:
    #        return goals
    #    else:
    #        return 0


    #def set_progress(self):
    #    self.progress = self.calculate_progress()

    #def calculate_progress(self):
    #    if self.goal_status == 'active' or self.goal_status == 'on hold':
    #        if self.effort_to_date > 0:  # work hasn't started
    #            if self.effort_remaining > 0:  # work has started and effort remains
    #                return float(self.effort_to_date) / float(self.effort_to_date + self.effort_remaining)
    #            else:  # work has started and no effort remains (essentially this is a complete action)
    #                return float(self.effort_to_date) / float(self.estimate)
    #        else:
    #            return 0
    #    elif self.goal_status == 'completed':
    #        return 1
    #    elif self.goal_status == 'not started' or self.goal_status == 'deleted':
    #        return 0
    #    else:
    #        return 0




class CourseThinDB(db.Model):
    course_name    = db.StringProperty(required=True)
    asset         = db.StringProperty(required=True)
    asset_key     = db.StringProperty(required=True)
    str_value     = db.StringProperty(required=False)
    int_value     = db.IntegerProperty(required=False)
    follower_count = db.IntegerProperty(required=False, default=0)
    course_tags   = db.StringListProperty()
    created       = db.DateTimeProperty(required=True, auto_now_add=True)
    #created_by      = db.ReferenceProperty(UserThinDB, collection_name='creator')
    updated       = db.DateTimeProperty(required=True, auto_now=True)
    #updated_by      = db.ReferenceProperty(UserThinDB, collection_name='updater')


class TopicThinDB(db.Model):
    topic_name    = db.StringProperty(required=True)
    asset         = db.StringProperty(required=True)
    asset_key     = db.StringProperty(required=True)
    str_value     = db.StringProperty(required=False)
    int_value     = db.IntegerProperty(required=False)
    follower_count = db.IntegerProperty(required=False, default=0)
    created       = db.DateTimeProperty(required=True, auto_now_add=True)
    #created_by      = db.ReferenceProperty(UserThinDB, collection_name='creator')
    updated       = db.DateTimeProperty(required=True, auto_now=True)
    #updated_by      = db.ReferenceProperty(UserThinDB, collection_name='updater')
    profile_pic     = db.BlobProperty(default=None)


class EventItem(polymodel.PolyModel):
    object_type = db.StringProperty()
    object_name = db.StringProperty()
    created = db.DateTimeProperty(required=True, auto_now_add=True)


class ArticleEvent(EventItem):
    article_url = ndb.StringProperty(required=True)
    article_title = ndb.StringProperty()
    article_image = ndb.StringProperty()
    creator      = ndb.KeyProperty(User)


class Activity(db.Model):
    actor = db.ReferenceProperty()
    message = db.TextProperty()
    object_type = db.StringProperty()
    action = db.StringProperty()
    created = db.DateTimeProperty(required=True, auto_now_add=True)


class ActivityIndex(db.Model):
    receivers = db.ListProperty(int)


class UserFollowerIndex(db.Model):
    followers       = db.ListProperty(int)


class TopicFollowerIndex(db.Model):
    followers       = db.ListProperty(int)


class ProjectFollowerIndex(db.Model):
    followers       = db.ListProperty(int)

class CourseFollowerIndex(db.Model):
    followers       = db.ListProperty(int)


class LikeIndex(db.Model):
    likers_id          = db.ListProperty(int)


class FollowingIndex(db.Model):
    following_id       = db.ListProperty(int)


class LikedIndex(db.Model):
    liked_id           = db.ListProperty(int)






class TeamThinDB(db.Model):
    team_name = db.StringProperty(required=True)
    created = db.DateTimeProperty(required=True, auto_now_add=True)


"""
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
    user          = db.ReferenceProperty(User, required = True)
    profile_pic   = db.BlobProperty(default=None)
    organization  = db.ReferenceProperty(Organization, required = False)
    created_at    = db.DateTimeProperty(auto_now_add = True)
    updated_at    = db.DateTimeProperty(auto_now = True)
    participation = db.RatingProperty()
    influence     = db.RatingProperty()
    feedback      = db.RatingProperty()
    contribution  = db.RatingProperty()
    attainment    = db.RatingProperty()
    servelife     = db.RatingProperty()
    ecosystem_ranking   = db.IntegerProperty()

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

# Rank is achievement level
class MemberRank(db.Model):
    member                      = db.ReferenceProperty(Member,required = True)
    rank                        = db.StringProperty(required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

class MemberFollowers(db.Model):
    followed                    = db.ReferenceProperty(Member, required = True)
    follower                    = db.ReferenceProperty(Member, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    unfollowed_at               = db.DateTimeProperty(required = False)

class MemberLikes(db.Model):
    member                      = db.ReferenceProperty(Member, required = True)
    liker                       = db.ReferenceProperty(Member, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    unliked_at                  = db.DateTimeProperty(required = False)    

class Team(db.Model):
    name                        = db.StringProperty(required = True)
    owner                       = db.ReferenceProperty(Member, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    profile_pic                 = db.BlobProperty(required = False)
    headline                    = db.StringProperty(required = False)
    description                 = db.StringProperty(required = False)
    team_type                   = db.StringProperty(required = True)
    influence                   = db.RatingProperty()
    feedback                    = db.RatingProperty()
    contribution                = db.RatingProperty()
    attainment                  = db.RatingProperty()
    servelife                   = db.RatingProperty()
    ecosystem_ranking           = db.IntegerProperty()
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

# Rank is achievement level
class TeamRank(db.Model):
    team                        = db.ReferenceProperty(Team, required = True)
    rank                        = db.StringProperty(required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

class TeamMember(db.Model):
    team                        = db.ReferenceProperty(Team, required = True)
    member                      = db.ReferenceProperty(Member, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    removed_at                  = db.DateTimeProperty(required = False)
    removed_reason              = db.StringProperty(required = False)
    removed_by                  = db.ReferenceProperty(Member, required = False)

class TeamFollower(db.Model):
    team                        = db.ReferenceProperty(Team, required = True)
    follower                    = db.ReferenceProperty(Member, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    unfollowed_at               = db.DateTimeProperty(required = False)
    #unfollowed_reason           = db.StringProperty(required = False)

class TeamLikes(db.Model):
    team                        = db.ReferenceProperty(Team, required = True)
    liker                       = db.ReferenceProperty(Member, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    unliked_at                  = db.DateTimeProperty(required = False)            

class Organization(db.Model):
    name                        = db.StringProperty(required = True)
    description                 = db.StringProperty(required = False)
    owner                       = db.ReferenceProperty(Member, required = True)
    organization_type           = db.StringProperty(required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    linkedin                    = db.LinkProperty(required = False)
    facebook                    = db.LinkProperty(required = False)
    twitter                     = db.StringProperty(required = False)
    website                     = db.LinkProperty(required = False)
    profile_pic                 = db.BlobProperty(default=None)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

class OrganizationMember(db.Model):
    organization                = db.ReferenceProperty(Organization, required = True)
    member                      = db.ReferenceProperty(Member, required = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    verified_at                 = db.DateTimeProperty(required = False)
    verified_by                 = db.ReferenceProperty(Member, required = False)
    removed_at                  = db.DateTimeProperty(required = False)
    removed_reason              = db.StringProperty(required = False)
    removed_by                  = db.ReferenceProperty(Member, required = False)

class Course(db.Model):
    name                        = db.StringProperty(required = True)
    number                      = db.StringProperty(required = False)
    organization                = db.ReferenceProperty(Organization, required = True)
    course_url                  = db.LinkProperty(required = False)
    headline                    = db.StringProperty(required = False)
    description                 = db.StringProperty(required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    owner                       = db.ReferenceProperty(Member, required = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

# Class - haven't figure this out. Course --> Class follows normal university structure. however you don't really have that with online courses. you take it when you want.
class CourseClass(db.Model):
    course                      = db.ReferenceProperty(Course, required = True)
    course_type                 = db.StringProperty(required = True)
    class_start                 = db.DateTimeProperty(required = False)
    owner                       = db.ReferenceProperty(Member, required = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

# Cohort - all them members of a class form a cohort.
class Cohort(db.Model):
    course_class                = db.ReferenceProperty(CourseClass, required = True)
    class_member                = db.ReferenceProperty(Member, required = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    verified_at                 = db.DateTimeProperty(required = False)
    verified_by                 = db.ReferenceProperty(Member, required = False)
    removed_at                  = db.DateTimeProperty(required = False)
    removed_reason              = db.StringProperty(required = False)
    removed_by                  = db.ReferenceProperty(Member, required = False)    

class Project(db.Model):
    name                        = db.StringProperty(required = True)
    headline                    = db.StringProperty(required = False)
    description                 = db.StringProperty(required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    owner                       = db.ReferenceProperty(Member, required = True)
    sponsor                     = db.ReferenceProperty(Organization, required = False)
    profile_pic                 = db.BlobProperty(required = False)
    status                      = db.StringProperty(required = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
   #followers calculated - don't know how to represent
   #likes calculated - don't know how to represent
   #riffs calculated - don't know how to represent
    influence                   = db.RatingProperty()
    feedback                    = db.RatingProperty()
    contribution                = db.RatingProperty()
    attainment                  = db.RatingProperty()
    servelife                   = db.RatingProperty()
    ecosystem_ranking           = db.IntegerProperty()
    #Need reference to parent project to track what project was riffed from

class ProjectFollower(db.Model):
    project                     = db.ReferenceProperty(Project, required = True)
    follower                    = db.ReferenceProperty(Member, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    unfollowed_at               = db.DateTimeProperty(required = False)
    #unfollowed_reason           = db.StringProperty(required = False)

# Rank is achievement level
class ProjectRank(db.Model):
    project                     = db.ReferenceProperty(Project, required = True)
    rank                        = db.StringProperty(required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

class ProjectMember(db.Model):
    project                     = db.ReferenceProperty(Project, required = True)
    member                      = db.ReferenceProperty(Member, required = True)
    team                        = db.ReferenceProperty(Team, required = False)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    removed_at                  = db.DateTimeProperty(required = False)
    removed_reason              = db.StringProperty(required = False)
    removed_by                  = db.ReferenceProperty(Member, required = False)

class ProjectLikes(db.Model):
    project                     = db.ReferenceProperty(Project, required = True)
    liker                       = db.ReferenceProperty(Member, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    unliked_at                  = db.DateTimeProperty(required = False) 

class ProjectGoals(db.Model):
    project                     = db.ReferenceProperty(Project, required = True)
    goal_name                   = db.StringProperty(required = True)
    goal_description            = db.StringProperty(required = False)
    sequence                    = db.IntegerProperty(required = True)
    status                      = db.StringProperty(required = True)
    active                      = db.BooleanProperty(required = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

#class ProjectMilestone (db.Model):
#class ProjectStory (db.Model):
#class ProjectTask (db.Model):
#class ProjectIteration (db.Model):

class Badge(db.Model):
    name                        = db.StringProperty(required = True)
    description                 = db.StringProperty(required = True)
    awarded_count               = db.IntegerProperty(required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    valid_at                    = db.DateTimeProperty(required = False)
    expires_at                  = db.DateTimeProperty(required = False)
    badge_image                 = db.BlobProperty(required = False)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)

class MemberBadge(db.Model):
    member                      = db.ReferenceProperty(Member, required = True)
    badge                       = db.ReferenceProperty(Badge, required = True)
    active                      = db.BooleanProperty(required = True, default = True)
    created_at                  = db.DateTimeProperty(required = True,auto_now_add = True)
    updated_at                  = db.DateTimeProperty(required = True,auto_now = True)
    #awarded_for

#TeamBadge
#ProjectBadge    
"""