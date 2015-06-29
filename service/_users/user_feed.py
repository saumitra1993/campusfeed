import logging
import webapp2
from google.appengine.ext import ndb
from service._channels._posts.posts import PostsHandler
from db.database import *
import json
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date

class UserFeed(webapp2.RequestHandler):
	"""docstring for UserFeed"""
	
	# RequestURL: /users/:user_id/feed GET
	# Response: user_id -> key -> 
	#			channels from channel_followers (=> channel keys) -> 
	#			key.get() (=> channels) -> 
	#			channel_ptr posts order by time
	# dict:{
	#  		'feed':[
	#             	{
    #            	  'channel_name':
    #              	  'channel_posts': [{},{}.....{}]
	#             	},
	#               {
	#                 'channel_name':
	#                 'channel_posts': [{},{}.....{}]
	#               }
	#              ]
	#      }

	def get(self,user_id):

		limit = int(self.request.get('limit'))
		offset = int(self.request.get('offset'))
		
		user_key = ndb.Key('Users', user_id)

		result = Channel_Followers.query(Channel_Followers.user_ptr == user_key)
		
		if limit != -1:
			user_followed_channels = result.fetch(limit,offset=offset)
		else:
			user_followed_channels = result.fetch(offset=offset)
		feed_array=[]
		dict_feed={}	
		if len(user_followed_channels)>0:	
			for user_followed_channel in user_followed_channels:	
				channel_ptr = user_followed_channel.channel_ptr
				# posts_handler = PostsHandler()
				# posts_of_channel = posts_handler.get(channel_ptr.id())
				# logging.warn(posts_of_channel)
				channel_details = Channels.get_by_id(user_followed_channel.channel_ptr.id())
				dict_={}
				if channel_details:
					dict_['channel_name'] = channel_details.channel_name

				out = []
				channel_posts = Channel_Admins.query(Channel_Admins.channel_ptr == channel_ptr).fetch()
				if len(channel_posts)>0:
					for channel_post in channel_posts:
						posting_user = Users.get_by_id(channel_post.user_ptr.id())
						_dict_channel_posts = {}
						_dict_channel_posts['post_id'] = channel_post.key.id()
						_dict_channel_posts['text'] = channel_post.text
						_dict_channel_posts['img_url'] = DEFAULT_ROOT_IMG_URL + str(channel_post.post_img_url)
						if post.isAnonymous == True:
							_dict_channel_posts['user_full_name'] = 'Anonymous'
						else:		
							_dict_channel_posts['user_full_name'] = posting_user.first_name+' '+posting_user.last_name
						_dict_channel_posts['created_time'] = date_to_string(utc_to_ist(channel_post.created_time))					
						_dict_channel_posts['user_img_url'] = str(posting_user.user_img_url)
						_dict_channel_posts['branch'] = posting_user.branch
						_dict_channel_posts['pending_bit'] = channel_post.pending_bit
						out.append(_dict_channel_posts)
			
				dict_['channel_posts'] = out
				feed_array.append(dict_)
			
			dict_feed['feed'] = feed_array
			self.response.set_status(200, 'Awesome')
		else:
				self.response.set_status(404, 'User is NOT following ANY channel')

		self.response.write(json.dumps(dict_feed))