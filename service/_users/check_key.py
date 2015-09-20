import webapp2
import logging
import json
from db.database import Users
from google.appengine.api import channel
from service._users.sessions import BaseHandler

class CheckKey(BaseHandler, webapp2.RequestHandler):
	def post(self):
		channel.send_message(
			'lock',
			self.request.body,
		)
		self.response.set_status(200,"Awesome!")