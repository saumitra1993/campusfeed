import webapp2
import logging
from service._users.login import Login
from service._users.image_url import ImageUrl
from service.get_photo import GetPhotu
from service._channels.get_my_channels import GetMyChannels
from service._channels.channels_handler import ChannelsHandler
from service._users.image_url import ImageUrl
from service._channels.image_url_channel import ChannelImageUrl
from service._channels._posts.image_url_post import PostImageUrl
from service._channels._posts.posts import PostsHandler
from service._channels._posts.approve_post import ApprovePost
from service._channels.channels import NewChannels
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
	('/users/(.*)/channels',GetMyChannels),
	#('/channels/<\d{16}>/posts',GetChannelPosts),
	('/channelimageurl',ChannelImageUrl),
    ('/postimageurl',PostImageUrl),
    ('/channels',NewChannels),
	webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>',ChannelsHandler),
    webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/posts',PostsHandler),
    webapp2.Route(r'/channels/<:[0-9a-zA-Z]{16}>/posts/<:[0-9][a-z][A-Z]{16}>',ApprovePost),
], config=config, debug=True)