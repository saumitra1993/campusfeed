import logging
import webapp2
import random
import string
import json
import hashlib
from datetime import datetime, timedelta
from handlers.mail import send_email
from db.database import Users, DBMobileAuth, DBUserGCMId, DBUserForgotPassword
from google.appengine.api import users
from service._users.sessions import BaseHandler
from google.appengine.ext import ndb
from service._users.authentication import get_password_hash, passwords_match
from const.constants import MOBILE_USER_SESSION_DURATION_DAYS

class ResetPassword(BaseHandler, webapp2.RequestHandler):

	def get(self):
		forgot_id = self.request.get('forgotId')
		hashed_id = hashlib.sha224(forgot_id).hexdigest()
		now = datetime.now()
		q = DBUserForgotPassword.query(DBUserForgotPassword.fid == hashed_id).fetch()
		if len(q) == 1:
			record = q[0]
			timestamp = record.creation_time
			if (now - timestamp).total_seconds() < 3600*48:
				self.response.set_status(200,'Let him reset boss.')
			else:
				self.response.set_status(401,'Fail')
		else:
			self.response.set_status(401,'Fail') 
		self.response.write(json.dumps({"tp":"kaddu"}))

	def post(self):
		data = json.loads(self.request.body)
		forgot_id = data.get('forgotId')
		password = data.get('password')
		hashed_id = hashlib.sha224(forgot_id).hexdigest()
		now = datetime.now()
		q = DBUserForgotPassword.query(DBUserForgotPassword.fid == hashed_id).fetch()
		if len(q) == 1:
			record = q[0]
			timestamp = record.creation_time
			if (now - timestamp).total_seconds() < 3600*48:
				user = record.user_ptr.get()
				new_password = get_password_hash(password)
				user.password = new_password
				user.put()
			else:
				self.response.set_status(401,'Fail')
		else:
			self.response.set_status(401,'Fail') 
		self.response.write(json.dumps({"tp":"kaddu"}))