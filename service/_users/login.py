import logging
import webapp2
import random
import string
import json
from datetime import datetime, timedelta
from db.database import Users, DBMobileAuth
from google.appengine.api import users
from service._users.sessions import BaseHandler
from service._users.authentication import get_password_hash, passwords_match
from const.constants import MOBILE_USER_SESSION_DURATION_DAYS

class Login(BaseHandler, webapp2.RequestHandler):
	"""docstring for Login"""
	# URL :- /login POST
	# Request params: user_id, password
	# Response : status, first_name,last_name
	# if success- 200
	# failure- 400
	def generate_and_store_mobile_token(self, user_id, name):
		mAuthToken = ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase+ string.digits, 32))
		
		db = DBMobileAuth(id=mAuthToken)
		db.name = name
		db.user_id = user_id
		db.expiration = datetime.now() + timedelta(days=MOBILE_USER_SESSION_DURATION_DAYS)
		db.put()
		return mAuthToken

	def post(self):
		logging.info("i am in Login")

		# db = Users()
		# db.first_name = self.request.get("first_name").strip()
		# db.last_name = self.request.get("last_name").strip()
		# db.branch = self.request.get("branch").strip()
		# db.phone = self.request.get("phone").strip()		
		# db.email_id = self.request.get("email_id").strip()
		# db.password = get_password_hash(self.request.get("password").strip())
		# db.user_id = self.request.get("user_id").strip()
		# db.user_img_url = self.get_uploads('user_img_url')[0].key()
		# db.put()
		# if users.is_current_user_admin():

		# 	password = self.request.get("password").strip()
		# 	result = User.query().filter(passwords_match(User.password, password)).fetch()
		# 	logging.info(result)
		# 	logging.info(users.get_current_user().nickname())
		# 	logging.info(users.is_current_user_admin())
		# else:
		# 	self.response.write("yay,,not working")

		# user_img_url = self.get_uploads('user_img_url')[0].key()
		# db.put()

		data = json.loads(self.request.body)
		# user_id = self.request.get("user_id").strip()
		# password = self.request.get("password").strip()
		user_id = data.get("user_id")
		password = data.get("password")
		logging.info(self.request)
		logging.info(user_id)
		result = Users.query().filter(Users.user_id == user_id).fetch()
		dict_={}
		if result:
			if(passwords_match(result[0].password, password)):
				dict_['first_name'] = result[0].first_name
				dict_['last_name'] = result[0].last_name
				mAuthToken = self.generate_and_store_mobile_token(user_id, result[0].first_name + result[0].last_name)
				dict_['mAuthToken'] = mAuthToken
				self.session['name'] = result[0].first_name + " " + result[0].last_name
				self.session['userid'] = result[0].key.id()
				self.session['last-seen'] = datetime.now()
				self.response.set_status(200, 'Awesome')
				self.response.write(json.dumps(dict_))
				logging.info("done")
			else:
				logging.info("Incorrect password.")
				self.response.set_status(401,'Fail')
		else:
			self.response.set_status(401,'Fail')


