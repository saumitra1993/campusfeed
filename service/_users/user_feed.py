import logging
import webapp2
from google.appengine.ext import ndb

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
		
