from google.appengine.ext import db

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
