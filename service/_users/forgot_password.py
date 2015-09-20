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

class ForgotPassword(BaseHandler, webapp2.RequestHandler):
	def post(self):
		data = json.loads(self.request.body)
		email = data.get('email_id')
		q = Users.query(Users.email_id == email).fetch()
		if len(q) == 1:
			user = q[0]
			forgotten = DBUserForgotPassword()
			forgot_id = self.id_generator()
			logging.info(forgot_id)
			hashed_id = hashlib.sha224(forgot_id).hexdigest()
			forgotten.fid = hashed_id
			forgotten.user_ptr = user.key
			forgotten.put()
			body = "Hello "+user.first_name+"! Greetings from Campusfeed team. So you forgot your password. No problem. Here is the link to reset it. http://campusfeedapp.com/web#resetpassword/"+forgot_id
			send_email("Link to reset password of your Campusfeed account",email,body)
			self.response.set_status(200,'Success!')
		else:
			self.response.set_status(401,'Fail')
		self.response.write(json.dumps({"tp":"kaddu"}))

	def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(20))