import logging
import webapp2
import random
import string
import json
import hashlib
from datetime import datetime, timedelta
from handlers.mail import send_email
from db.database import Users, DBMobileAuth, DBUserGCMId, DBUserForgotPassword, DBUserChannelId
from google.appengine.api import users
from service._users.sessions import BaseHandler
from google.appengine.ext import ndb
from service._users.authentication import get_password_hash, passwords_match
from const.constants import MOBILE_USER_SESSION_DURATION_DAYS

class ChannelId(BaseHandler, webapp2.RequestHandler):
	def get(self):
		user_id =  int(self.request.get('user_id'))
		user = Users.get_by_id(user_id)
		if user:
			channel_exists = DBUserChannelId.query(DBUserChannelId.user_ptr == user.key).fetch()
			if len(channel_exists) == 0:
				first_name = user.first_name
				last_name = user.last_name
				start = len(first_name)/2
				last = len(last_name)/2
				channel_id = first_name[:start]+last_name[:last]
				channel = DBUserChannelId()
				channel.user_ptr = user.key
				channel.channel_id = channel_id
				channel.put()
				_dict = {}
				_dict['channel_id'] = channel_id
			else:
				_dict = {}
				_dict['channel_id'] = channel_exists[0].channel_id
			self.response.write(json.dumps(_dict))
		else:
			self.response.set_status(400,'User not there')
