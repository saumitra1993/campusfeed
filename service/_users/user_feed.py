import logging
import webapp2
from google.appengine.ext import ndb
from service._channels._posts.posts import PostsHandler

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
    #              	  'posts': [{},{}.....{}]
	#             	},
	#               {
	#                 'channel_name':
	#                 'posts': [{},{}.....{}]
	#               }
	#              ]
	#      }

	def get(self,user_id):

		limit = self.request.get('limit')
		offset = self.request.get('offset')
		
		user_key = ndb.Key('Users', user_id)

		result = Channel_Followers.query(Channel_Followers.user_ptr == user_key)
		
		if limit != -1:
			user_followed_channels = result.fetch(limit,offset=offset)
		else:
			user_followed_channels = result.fetch(offset=offset)

		for user_followed_channel in user_followed_channels:	
			channel_ptr = user_followed_channel.channel_ptr
			posts_handler = PostsHandler()
			posts_of_channel = posts_handler.get(channel_ptr.id())
			logging.warn(posts_of_channel)