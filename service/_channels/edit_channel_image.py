import logging
import webapp2
import random
import string
import json
from db.database import Channels

class EditChannelImage(webapp2.RequestHandler):
	"""docstring for EditUserImage"""
	
	def post(self):

		image = self.request.get('channel_img')
		channel_id = self.request.get('channel_id').strip()

		if image!='':
			image = images.Image(image)
			# Transform the image
			image.resize(width=200, height=200)
			image = image.execute_transforms(output_encoding=images.JPEG)
			size = len(image)
			if size > 1000000:
				self.response.set_status(400,"Image too big")
				return

		result = Channels.query(Users.channel_id == channel_id)
		channel_exists = result.fetch()

		if channel_exists:
			db = Channels()
			if image!='':
				db.img = image
			else:
				db.img = ''
			db.put()
			self.response.set_status(200,"Awesome")
		else:
			self.response.set_status(400,"User is malicious. Tell him to fuck himself.")