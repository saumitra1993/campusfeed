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
		user_id = int(user_id)
		gcm_id = data.get("gcm_id").strip()
		logging.info("%s"%user_id)
		logging.info("%s"%gcm_id)
		user = Users.get_by_id(user_id)
		dict_ = {}
		dict_['gcm_response'] = "blah"
		if user:
			logging.info(user)
			user_ptr = user.key
			q = DBUserGCMId.query(DBUserGCMId.user_ptr == user_ptr).fetch()
			if len(q) == 0:
				db = DBUserGCMId()
				db.user_ptr = user_ptr
				db.gcm_id = gcm_id
				db.put()
			else:
				q[0].gcm_id = gcm_id

			self.response.set_status(200,"Awesome")
		else:
			self.response.set_status(400,"User is malicious.Tell him to go fuck himself.")
		self.response.write(json.dumps(dict_))