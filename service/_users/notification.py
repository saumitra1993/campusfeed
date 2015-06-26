import webapp2
import logging
import json
from db.database import Channels, Users, Channel_Admins
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID
from service._users.sessions import BaseHandler
from google.appengine.ext import ndb

class Notifications(BaseHandler, webapp2.RequestHandler):

	# Request URL: users/:userid/notifications GET
	# Response:
	#  dict: {
	#     'admin_notif': channel_id, channe_name, user_id, user_first_name,lastname,bit  #admin added/removed
	#     'channel_notif': 
	#     'post_notif':
	#     'upvote_notif':
	#     'follow_notif':
	#  }
	def get(self, user_id):
		user_query = Users.query(Users.user_id == user_id)
		result = user_query.fetch()
		if len(result) == 1:
			user = result[0]
			lastSeen = self.session['last-seen']
			if user.type_ == 'admin':
				admins_to_new_channels = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.created_time > lastSeen).fetch()
				admins