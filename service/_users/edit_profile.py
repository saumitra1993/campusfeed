import webapp2
import logging
from db.database import Users

class EditProfile(webapp2.RequestHandler):
	"""docstring for EditProfile"""
	
	# Request URL - /users/:user_id PUT
	# Request params - email_id, user_phone
	# Response - status
	
	def put(self,user_id):
		email_id = self.request.get('email_id')
		phone = self.request.get('phone')

		result = Users.query(Users.user_id == user_id).fetch()
		if result==1:
			db=Users()
			
			if email_id:
				db.email_id = email_id
				eflag=1
			if phone:
				db.phone = phone
				pflag=1

			db.put()
			if eflag==1:
				self.response.set_status(200,'Awesome.Email_id updated.')
			elif pflag==1:
				self.response.set_status(200,'Awesome.Phone# updated.')
			else:	
				self.response.set_status(200,'Awesome.Email_id n Phone# updated.')
		else:
			self.response.set_status(401,'User sucks.He has no entry.')

			

		

