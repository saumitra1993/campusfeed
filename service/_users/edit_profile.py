import webapp2
import logging
from db.database import Users
from service._users.sessions import BaseHandler

class Profile(BaseHandler, webapp2.RequestHandler):
	"""docstring for EditProfile"""
	
	# Request URL - /users/:user_id PUT
	# Request params - email_id, user_phone
	# Response - status
	
	def put(self,user_id):
		email_id = self.request.get('email_id')
		phone = self.request.get('phone')

		result = Users.query(Users.user_id == user_id).fetch()
		if len(result) == 1:
			user = result[0]
			
			if email_id:
				user.email_id = email_id
				eflag = 1
			if phone:
				user.phone = phone
				pflag = 1

			user.put()
			self.session['last-seen'] = datetime.now()
			if eflag == 1:
				self.response.set_status(200,'Awesome.Email_id updated.')
			elif pflag == 1:
				self.response.set_status(200,'Awesome.Phone# updated.')
			else:	
				self.response.set_status(200,'Awesome.Email_id n Phone# updated.')
		else:
			self.response.set_status(401,'User sucks.He has no entry.')

			

		

