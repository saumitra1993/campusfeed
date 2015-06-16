import logging
import webapp2
from database import User
from google.appengine.api import users
from authentication import get_password_hash, passwords_match

class Login(webapp2.RequestHandler):
	"""docstring for Login"""

	# def __init__(self, arg):
	# 	super(Login, self).__init__()
	# 	self.arg = arg
	def post(self):
		logging.info("i am in Login")

		# db = User()
		# db.username = self.request.get("username").strip()
		# db.branch = self.request.get("branch").strip()
		# db.phone = self.request.get("phone").strip()		
		# db.email_id = self.request.get("email_id").strip()
		# db.password = get_password_hash(self.request.get("password").strip())
		# db.put()
		if users.is_current_user_admin:

			password = self.request.get("password").strip()
			result = User.query().filter(passwords_match(User.password, password)).fetch()
			logging.info(result)
			logging.info(users.get_current_user())
			logging.info(users.is_current_user_admin())
		else:
			self.response.write("Fuck off")