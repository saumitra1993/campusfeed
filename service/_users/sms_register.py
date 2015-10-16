__author__ = 'Saumitra'

import webapp2
import os
import logging
import json
from handlers.push import push_dict
from db.database import *

class SMSRegister(webapp2.RequestHandler):
		def get(self):
			 
			self.response.write(open('templates/axisreg.html').read())


		def post(self):
			data = json.loads(self.request.body)
			phone_number = data.get('phone_number')
			logging.info(phone_number)
			text = "Hi! Welcome to AXIS 2015! \n Visit this link to get updates - http://campusfeedapp.com/web#/channels/related/5663052624035840 \n -Campusfeed Team"
			message = {}
			message['message'] = text 
			users = Users.query(Users.user_id == "14098").fetch()
			if len(users) == 1:
				user = users[0]
				gcm_user = DBUserGCMId.query(DBUserGCMId.user_ptr == user.key).fetch()
				if len(gcm_user) == 1:
					gcm_id = gcm_user[0].gcm_id
					message['phone_number'] = phone_number
					push_dict(gcm_id, message)
					self.response.set_status(200, "Awesome")
				else:
					self.response.set_status(401, "No gcm id")
					logging.info("No gcm id")
			else:
				self.response.set_status(401, "No gcm id")
				logging.info("No user? What!!!")