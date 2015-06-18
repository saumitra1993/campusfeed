import webapp2
import logging
import json

class GetMyChannels(object):
	"""docstring for GetMyChannels"""
	# Request URL- /users/:user_id/channels GET
	# Response - Dictionary of status(200/400), user_channels: array of (   channel_id, 
	# 																		channel_name, 
	# 																		channel_img_url, 
	# 																		num_followers)
	# Query params-
	# limit and offset

	def get(self,user_id):
		self.response.write(user_id)

			
