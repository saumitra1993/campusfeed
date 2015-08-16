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
			image.resize(width=200, height=200)
			image = image.execute_transforms(output_encoding=images.JPEG)
			size = len(image)
			if size > 1000000:
				self.response.set_status(400,"Image too big")
				return
		
		result = Users.query(ndb.OR((Users.user_id == user_id),(Users.email_id == email_id)))
		user_already_exists = result.fetch()

		if user_already_exists:
			self.response.set_status(400,"User Already Exists")
		elif len(user_already_exists) == 0:
			new_password = get_password_hash(password)
			
			db = Users()
			db.email_id = email_id
			db.user_id = user_id
			db.password = new_password
			db.first_name = first_name
			db.last_name = last_name
			db.branch = branch
			db.phone = phone
			if image!='':
				db.img = image
			else:
				db.img = ''
			db.put()
			self.response.set_status(200,"Awesome")