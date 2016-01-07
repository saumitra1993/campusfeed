import webapp2
import logging
from handlers.home import Home
from handlers.webhome import WebHome
from handlers.contest import GuestHandler
from handlers.lock import LockHandler

from tasks.gcm_push import PushMsg

from service.get_photo import GetPhotu
#from service._users.login import Login
from service._users.signup import Signup
from service._users.image_url import ImageUrl
from service._users.search_users import SearchUsers
from service._users.edit_profile import Profile
from service._users.requests import PendingChannels
from service._users.userid_gcmid import UserIdGcmId
from service._users.logout import LogoutUser
from service._users.edit_user_image import EditUserImage
from service._users.user_feed import UserFeed
from service._users.notification import Notifications
from service._users.forgot_password import ForgotPassword
from service._users.reset_password import ResetPassword
from service._users.feedback import Feedback
from service._users.superuserfollow import SuperuserFollow
from service._users.check_key import CheckKey
from service._users.channeltoken import ChannelToken
from service._users.channelid import ChannelId
from service._users.sms_register import SMSRegister 

from service._channels.followed_channels import FollowedChannels
from service._channels.delete_channel_follower import DeleteChannelFollower
from service._channels.channels_handler import ChannelsHandler
from service._channels.image_url_channel import ChannelImageUrl
from service._channels.channels import AllChannels
from service._channels.my_channels import MyChannels
from service._channels.channel_admins import ChannelAdmins
from service._channels.channel_followers import ChannelFollowers
from service._channels.search_channel import SearchChannels
from service._channels.edit_channel_image import EditChannelImage

from service._channels._threads.threads import ThreadsHandler
from service._channels._threads.delete_thread import RemoveThreadHandler
from service._channels._threads.delete_thread_comment import RemoveCommentHandler
from service._channels._threads.thread_discussions import ThreadDiscussionsHandler

from service._channels._posts.image_url_post import PostImageUrl
from service._channels._posts.posts import PostsHandler
from service._channels._posts.files import GetFile
from service._channels._posts.file_upload_endpoint import PostUploadURL
from service._channels._posts.view_post import PostViewed
from service._channels._posts.approve_post import OnePost
from service.ig.updateresult import UpdateResult
from service.ig.eventtime import EventTime

config = {}
config['webapp2_extras.sessions'] = {
	'secret_key': 'qwertyuioppoiuytrewqqwertyuiopsdfkjbsdjf',
	'session_max_age': None,
	'cookie_args': {
        'max_age':     2592000,
        'domain':      None,
        'path':        '/',
        'secure':      None,
        'httponly':    False,
    },
	'backends': {'datastore': 'webapp2_extras.appengine.sessions_ndb.DatastoreSessionFactory',
                 'memcache': 'webapp2_extras.appengine.sessions_memcache.MemcacheSessionFactory',
                 'securecookie': 'webapp2_extras.sessions.SecureCookieSessionFactory'}
}

logging.getLogger().setLevel(logging.DEBUG)
application = webapp2.WSGIApplication([
	#Services
	#('/', MyClassName),
	('/',Home),
	('/web',WebHome),
	#('/login',Login),
	('/signup',Signup),
	('/imageurl',ImageUrl),
	('/register', SMSRegister),
	('/pic/(.*)',GetPhotu),
	('/files/(.*)',GetFile),
	('/channelimageurl',ChannelImageUrl),
	('/forgotpassword', ForgotPassword),
	('/resetpassword', ResetPassword),
	('/feedback',Feedback),

	('/pushnotif',UserIdGcmId),
	('/logout',LogoutUser),
	('/edituserimage',EditUserImage),
	('/editchannel',EditChannelImage),
	('/checkkey',CheckKey),

	('/postimageurl',PostImageUrl),
	('/channels',AllChannels),
	('/superuserfollow', SuperuserFollow),
	('/uploadendpoint', PostUploadURL),
	('/channelid', ChannelId),

	('/tasks/pushmsg', PushMsg),

	webapp2.Route(r'/users/<:[0-9a-zA-Z]{16}>',Profile),
	webapp2.Route(r'/users/<:[0-9a-zA-Z]{16}>/channels',FollowedChannels),
	webapp2.Route(r'/users/<:[0-9a-zA-Z]{16}>/unfollowchannel',DeleteChannelFollower),
	webapp2.Route(r'/users/<:[0-9a-zA-Z]{16}>/mychannels',MyChannels),
	webapp2.Route(r'/users/<:[0-9a-zA-Z]{16}>/pendingchannels', PendingChannels),
	webapp2.Route(r'/users/search', SearchUsers),

	webapp2.Route(r'/users/<:[0-9a-zA-Z]{16}>/feed',UserFeed),

	webapp2.Route(r'/users/<:[0-9a-zA-Z]{16}>/notifications', Notifications),

	webapp2.Route(r'/key',GuestHandler),
	webapp2.Route(r'/lock',LockHandler),
	webapp2.Route('/channeltoken', ChannelToken),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>',ChannelsHandler),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/followers',ChannelFollowers),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/admins',ChannelAdmins),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/posts/<:[0-9a-zA-Z]{16}>',OnePost),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/posts',PostsHandler),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/threads/<:[0-9a-zA-Z]{16}>/discussions',ThreadDiscussionsHandler),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/threads/<:[0-9a-zA-Z]{16}>/deletecomment',RemoveCommentHandler),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/threads',ThreadsHandler),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/deletethread',RemoveThreadHandler),
	webapp2.Route(r'/channels/search',SearchChannels),
	webapp2.Route(r'/posts/<:[0-9a-zA-Z]{16}>/views', PostViewed),

	webapp2.Route(r'/updateresult',UpdateResult),
	webapp2.Route(r'/eventtime', EventTime),

], config=config, debug=True)