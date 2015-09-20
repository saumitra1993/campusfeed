import webapp2
import json
import logging
from datetime import datetime, timedelta
from service._users.sessions import BaseHandler, LoginRequired
from handlers.push import push_dict
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import TaskRetryOptions
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, DEFAULT_ANON_IMG_URL
from db.database import Users, Channels, Posts, Channel_Admins, Views, Channel_Followers, DBUserGCMId
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.ext import ndb

class PushMsg(webapp2.RequestHandler):
	""" This handler is invoked as a task. Never to be directly invoked 
		Any error in this task will make the task execute again
	"""
	def post(self):
		channel_id = int(self.request.get('channel_id'))
		user_id = int(self.request.get('user_id'))
		message = self.request.get('message')
		channel = Channels.get_by_id(channel_id)
		user = Users.get_by_id(user_id)
		logging.info("Task channel_id and user_id %s %s"%channel_id%user_id)
		if channel and user:
			channel_ptr = channel.key
			user_ptr = user.key
			result = Channel_Followers.query(Channel_Followers.getNotification == 1, Channel_Followers.channel_ptr == channel_ptr, Channel_Followers.user_ptr != user_ptr, Channel_Followers.isDeleted == 0)
			notify_these_users = result.fetch()

			
			for user in notify_these_users:
				user_ptr = user.user_ptr
				user_gcm_id = DBUserGCMId.query(DBUserGCMId.user_ptr == user_ptr).fetch()
				if len(user_gcm_id) == 1:
					gcm_id = user_gcm_id[0].gcm_id
					push_dict(gcm_id, message)
		else:
			logging.error('User or channel not valid %s %s'%user_id%channel_id)
