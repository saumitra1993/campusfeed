import webapp2
import json
import logging
from datetime import datetime
from google.appengine.api import blobstore
from service._users.sessions import BaseHandler
from db.database import Users, Channel_Admins, Channels, Channel_Followers
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.ext import ndb
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID

class ChannelImageHandler(BaseHandler,webapp2.RequestHandler):
	"""docstring for ChannelImage"""
	def post(self, type_):
		#Type will either be the channel id to which you want to add an image or the word 'new'
		type_ = str(type_)
		image = self.request.get('channel_img')
		dict_ = {}
		if image!='':
			image = images.Image(image)
			# Transform the image
			image.resize(width=400, height=400)
			image = image.execute_transforms(output_encoding=images.JPEG)
			size = len(image)
			if size > 1000000:
				self.response.set_status(400,"Image too big")
				return
			if type_ == 'new':
				db = Channels()
				db.img = image
				k = db.put()
				dict_['channel_id'] = k.id()
		else:
			self.response.set_status(400,"No image")