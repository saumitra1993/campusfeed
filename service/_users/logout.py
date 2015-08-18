import logging
import webapp2
import random
import string
import json
from datetime import datetime, timedelta
from db.database import Users, DBMobileAuth, DBUserGCMId
from google.appengine.api import users
from service._users.sessions import BaseHandler
from google.appengine.ext import ndb
from service._users.authentication import get_password_hash, passwords_match
from const.constants import MOBILE_USER_SESSION_DURATION_DAYS

class LogoutUser(BaseHandler, webapp2.RequestHandler):
	"""docstring for LogoutUser"""
	
	def post(self):

		mob_auth_token = self.request.get("mob_auth_token").strip()
		mob_auth_token = str(mob_auth_token)
		users_mob_auth = DBMobileAuth.get_by_id(mob_auth_token)
		
		if users_mob_auth:
			user_key = users_mob_auth.key
			user_key.delete()
			self.response.set_status(200,"Awesome")
		else:
			self.response.set_status(400,"No user with this Mob Auth Token")