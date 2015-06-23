import webapp2
import logging
from service.get_photo import GetPhotu

from service._users.login import Login
from service._users.image_url import ImageUrl
from service._users.edit_profile import EditProfile
from service._users.search_users import SearchUsers

from service._channels.followed_channels import FollowedChannels
from service._channels.channels_handler import ChannelsHandler
from service._channels.image_url_channel import ChannelImageUrl
from service._channels.channels import AllChannels
from service._channels.my_channels import MyChannels
from service._channels.channel_admins import ChannelAdmins

from service._channels._posts.image_url_post import PostImageUrl
from service._channels._posts.posts import PostsHandler
from service._channels._posts.approve_post import ApprovePost
from service._channels._posts.upvote_post import UpvotePost

config = {}
config['webapp2_extras.sessions'] = {
	'secret_key': 'qwertyuioppoiuytrewqqwertyuiopsdfkjbsdjf'
}

logging.getLogger().setLevel(logging.DEBUG)
application = webapp2.WSGIApplication([
	#Services
	#('/', MyClassName),
	('/login',Login),
	('/imageurl',ImageUrl),
	('/pic/(.*)',GetPhotu),
	('/users/(.*)/channels',FollowedChannels),
	('/users/(.*)/mychannels',MyChannels),
	('/channelimageurl',ChannelImageUrl),
    ('/postimageurl',PostImageUrl),
    ('/channels',AllChannels),
    webapp2.Route(r'/users/search',SearchUsers)
    webapp2.Route(r'/users/<:[0-9]{5}>',EditProfile),
	webapp2.Route(r'/channels/<:[0-9][a-z][A-Z]{16}>',ChannelsHandler),
	webapp2.Route(r'/channels/<:[0-9][a-z][A-Z]{16}>/admins',ChannelAdmins),
    webapp2.Route(r'/channels/<:[0-9][a-z][A-Z]{16}>/posts',PostsHandler),
    webapp2.Route(r'/channels/<:[0-9][a-z][A-Z]{16}>/posts/<:[0-9][a-z][A-Z]{16}>',ApprovePost),
    webapp2.Route(r'/posts/<:[0-9][a-z][A-Z]{16}>/upvotes',UpvotePost),
	#('/channels/<\d{16}>/posts',GetChannelPosts),
], config=config, debug=True)