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
from operator import itemgetter
from service._users.authentication import get_password_hash, passwords_match

class Signup(webapp2.RequestHandler):
	"""docstring for Signup"""

	def post(self):

		
		image = self.request.get('user_img')
		user_id = self.request.get('user_id')
		first_name = self.request.get('first_name')
		last_name = self.request.get('last_name')
		email_id = self.request.get('email_id')
		password = self.request.get('password')
		branch = self.request.get('branch')
		phone = self.request.get('phone')
		if image!='':
			image = images.Image(image)
			# Transform the image
			image.resize(width=400, height=400)
			image = image.execute_transforms(output_encoding=images.JPEG)
			size = len(image)
			if size > 1000000:
				self.response.set_status(400,"Image too big")
				return
		
		
		pw = get_password_hash(password)
		a = Users()
		a.user_id = user_id
		a.first_name = first_name
		a.last_name = last_name
		a.email_id = email_id
		a.password = password
		a.branch = branch
		a.phone = phone
		a.password = pw
		if image != '':
			a.img = image
		else:
			a.img = ''
		a.put()
		self.response.set_status(200,"Awesome")