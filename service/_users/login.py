import logging
import webapp2
from db.database import Users
from google.appengine.api import users
from service._users.authentication import get_password_hash, passwords_match
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class Login(blobstore_handlers.BlobstoreUploadHandler):
	"""docstring for Login"""
	# URL :- /login POST
	# Request params: user_id, password
	# Response : status, first_name,last_name
	# if success- 200
	# failure- 400
	
	def post(self):
		logging.info("i am in Login")

		db = Users()
		db.first_name = self.request.get("first_name").strip()
		db.last_name = self.request.get("last_name").strip()
		db.branch = self.request.get("branch").strip()
		db.phone = self.request.get("phone").strip()		
		db.email_id = self.request.get("email_id").strip()
		db.password = get_password_hash(self.request.get("password").strip())
		db.user_id = self.request.get("user_id").strip()
		db.user_img_url = self.get_uploads('user_img_url')[0].key()
		db.put()
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

		
		# db.user_id = self.request.get("user_id").strip()
		# password = self.request.get("password").strip()
		# db.password = get_password_hash(password)

		# result = User.query().filter(User.user_id == user_id).fetch()
		# dict_={}
		# if result:
		# 	if(passwords_match(User.password, password)):
		# 		dict_['first_name'] = result[0].first_name
		# 		dict_['last_name'] = result[0].last_name
		# 		dict_['status'] = '200'
		# 		self.response.write(json.dumps(dict_))
		# 	else:
		# 		logging.info("Incorrect password.")
		# else:
		# 	logging.info("Login Failed!")	

