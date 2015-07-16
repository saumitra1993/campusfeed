import webapp2
import logging
from handlers.home import Home
from handlers.webhome import WebHome

from service.get_photo import GetPhotu

from service._users.login import Login
from service._users.image_url import ImageUrl
from service._users.search_users import SearchUsers
from service._users.edit_profile import Profile
from service._users.requests import PendingChannels

from service._users.user_feed import UserFeed

from service._users.notification import Notifications


from service._channels.followed_channels import FollowedChannels
from service._channels.channels_handler import ChannelsHandler
from service._channels.image_url_channel import ChannelImageUrl
from service._channels.channels import AllChannels
from service._channels.my_channels import MyChannels
from service._channels.channel_admins import ChannelAdmins
from service._channels.channel_followers import ChannelFollowers
from service._channels.search_channel import SearchChannels

from service._channels._posts.image_url_post import PostImageUrl
from service._channels._posts.posts import PostsHandler
from service._channels._posts.upvote_post import UpvotePost
from service._channels._posts.approve_post import OnePost

config = {}
config['webapp2_extras.sessions'] = {
	'secret_key': 'qwertyuioppoiuytrewqqwertyuiopsdfkjbsdjf',
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
	('/login',Login),
	('/imageurl',ImageUrl),
	('/pic/(.*)',GetPhotu),
	('/channelimageurl',ChannelImageUrl),

	('/postimageurl',PostImageUrl),
	('/channels',AllChannels),
	webapp2.Route(r'/users/<:[0-9a-zA-Z]{5}>',Profile),
	webapp2.Route(r'/users/<:[0-9a-zA-Z]{5}>/channels',FollowedChannels),
	webapp2.Route(r'/users/<:[0-9a-zA-Z]{5}>/mychannels',MyChannels),
	webapp2.Route(r'/users/<:[0-9a-zA-Z]{5}>/pendingchannels', PendingChannels),
	webapp2.Route(r'/users/search', SearchUsers),

	webapp2.Route(r'/users/<:[0-9a-zA-Z]{5}>/feed',UserFeed),

	webapp2.Route(r'/users/<:[0-9a-zA-Z]{5}>/notifications', Notifications),


	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>',ChannelsHandler),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/followers',ChannelFollowers),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/admins',ChannelAdmins),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/posts',PostsHandler),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/posts/<:[0-9][a-z][A-Z]{16}>',OnePost),
	webapp2.Route(r'/channels/search',SearchChannels),
	webapp2.Route(r'/posts/<:[0-9a-zA-Z]{16}>/upvotes',UpvotePost),

], config=config, debug=True)