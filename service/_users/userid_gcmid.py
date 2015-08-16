import logging
import webapp2
import random
import string
import json
from datetime import datetime, timedelta
from db.database import Users, DBMobileAuth, DBUserGCMId
from google.appengine.api import users

class UserIdGcmId(webapp2.RequestHandler):
	"""docstring for UserIdGcmId"""
	
	def post(self):

		user_id = self.request.get("user_id").strip()
		gcm_id = self.request.get("gcm_id").strip()

		user_query = Users.query(Users.user_id == user_id).fetch()

		if len(user_query) == 1 :
			user = user_query[0]
			user_ptr = user.key

			db = DBUserGCMId()
			db.user_ptr = user_ptr
			db.gcm_id = gcm_id
			db.put()

			self.response.set_status(200,"Awesome")
		else:
			self.response.set_status(400,"User is malicious.Tell him to go fuck himself.")