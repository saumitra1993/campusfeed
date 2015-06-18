import webapp2
import json
import logging

class Channels(object):
	"""docstring for Channels"""
	# Request URL - /channels POST
	# Request params - user_id, channel_name, channel_img, description, curated_bit
	# Response - status

	def post(self):
		