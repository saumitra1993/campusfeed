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
		data = json.loads(self.request.body)
		user_id = data.get("user_id").strip()
		gcm_id = data.get("gcm_id").strip()
		logging.info("%s"%user_id)
		logging.info("%s"%gcm_id)
		user_query = Users.query(Users.user_id == user_id).fetch()

		if len(user_query) == 1:
			user = user_query[0]
			logging.info(user)
			user_ptr = user.key

			db = DBUserGCMId()
			db.user_ptr = user_ptr
			db.gcm_id = gcm_id
			db.put()

			self.response.set_status(200,"Awesome")
		else:
			self.response.set_status(400,"User is malicious.Tell him to go fuck himself.")