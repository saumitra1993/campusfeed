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

class Feedback(BaseHandler, webapp2.RequestHandler):
	def post(self):
		name = self.request.get('name')
		email = self.request.get('email')
		message = self.request.get('comment')
		logging.info(message)
		body = "Hello superusers! The message sent from user having mail id "+email+" and name "+name+" is--"+message
		send_email("Message from user","support@campusfeedapp.com",body)
		self.response.set_status(200,'Success!')
		self.response.write("<h2 style='text-align:center;margin-top:20%;'>Thank you so much for the feedback! We will get right back to you with a response! :)</h2>")