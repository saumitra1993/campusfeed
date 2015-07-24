import webapp2
import logging
import json
from datetime import datetime, timedelta
from db.database import Channels, Users, Channel_Admins, Channel_Followers
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID

class ChannelFollowers(webapp2.RequestHandler):
	"""docstring for ChannelFollowers"""
	
	# RequestURL : /channels/:channel_id/followers GET
	# Response: array[
	#  {
	#   'user_id':
	#   'user_img_url':
	#   'user_name':
	#  },
	#  {...},
	# ]

	def get(self,channel_id):

		channel = Channels.get_by_id(int(channel_id))
		dict_ = {}
		if channel:
			channel_followers_details = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key).fetch()
			if len(channel_followers_details)>0:
				jarray=[]
				for channel_follower_details in channel_followers_details:
					user = Users.get_by_id(int(channel_follower_details.user_ptr.id()))
					if user:
						_dict={}
						_dict['user_id'] = user.user_id # id of the user following the channel
						_dict['user_full_name'] = user.first_name + ' ' + user.last_name
						_dict['user_img_url'] = DEFAULT_ROOT_IMG_URL + str(user.key.urlsafe())
						jarray.append(_dict)
				
				dict_['channel_followers'] = jarray
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(404, 'Given channel has NO followers.')
		else:
			self.response.set_status(400, 'Channel not found')

		self.response.write(json.dumps(dict_))
