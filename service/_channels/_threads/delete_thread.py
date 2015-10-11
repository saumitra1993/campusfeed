import webapp2
import json
import logging
from datetime import datetime, timedelta
from service._users.sessions import BaseHandler, LoginRequired
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, DEFAULT_ANON_IMG_URL
from db.database import *
from google.appengine.ext import ndb

class RemoveThreadHandler(BaseHandler,webapp2.RequestHandler):
	"""docstring for Threads"""
	# Request URL - /channels/:channel_id/deletethread POST
	# Request Params - channel_id(generated),thread_id
	# Response - status
	# if curated_bit is not set, status = 200
	
	@LoginRequired
	def post(self,channel_id):

		user_id = self.userid
		user_id = int(user_id)
		data = json.loads(self.request.body)
		thread_id = data.get('thread_id').strip()
		dict_ = {}
		
		user = Users.get_by_id(user_id)
		if user:
			user_ptr = user.key
			channel_id = int(channel_id)
			channel = Channels.get_by_id(channel_id)
			thread_id = int(thread_id)
			thread = Threads.get_by_id(thread_id)
			if channel and thread:
				channel_ptr = channel.key
				thread_ptr = thread.key
				is_admin = Channel_Admins.query(Channel_Admins.channel_ptr == channel_ptr, Channel_Admins.user_ptr == user_ptr, Channel_Admins.isDeleted == 0).count()
				
				if is_admin == 1:				
					thread.isDeleted = 1
					thread.put()

					self.response.set_status(200, 'Awesome')
				else:
					self.response.set_status(400, 'Not admin')
					logging.info('Not admin')
				#-----------------------------------------------------------	
			else:
				self.response.set_status(401, 'Invalid channel or thread')
				logging.info('Invalid channel or thread')
		else:
			self.response.set_status(401, 'Invalid user')

		self.response.write(json.dumps(dict_))
