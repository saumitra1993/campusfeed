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
			message['phone_number'] = phone_number
			s = DBPhoneNumbers()
			s.number = phone_number
			s.put()
			users = Users.query(Users.user_id == "14098").fetch()
			dict_ = {}
			dict_['gcm_response'] = "blah"
			if len(users) == 1:
				user = users[0]
				user_ids = DBProxyUserGCMId.query(DBProxyUserGCMId.user_ptr == user.key).fetch()
				sent = 0
				for user_id in user_ids:
					if sent == 0:
						if user_id.message_count < 100:
							user_id.message_count = user_id.message_count + 1
							user_id.put()
							sent = 1
							push_dict(user_id.gcm_id, message)
						else:
							logging.error("One phone exhausted!")
					else:
						break
				
				self.response.set_status(200, "Awesome")	
				self.response.write(json.dumps(dict_))
			else:
				self.response.set_status(401, "No gcm id")
				logging.info("No user? What!!!")