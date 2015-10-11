import webapp2
import json
import logging
from datetime import datetime, timedelta
from service._users.sessions import BaseHandler, LoginRequired
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, DEFAULT_ANON_IMG_URL
from db.database import *
from google.appengine.ext import ndb

class RemoveCommentHandler(BaseHandler,webapp2.RequestHandler):
	"""docstring for Threads"""
	# Request URL - /channels/:channel_id/threads/:thread_id/deletecomment POST
	# Request Params - channel_id(generated),thread_id
	# Response - status
	# if curated_bit is not set, status = 200
	
	@LoginRequired
	def post(self,channel_id,thread_id):

		user_id = self.userid
		user_id = int(user_id)
		data = json.loads(self.request.body)
		comment_id = data.get('comment_id').strip()
		dict_ = {}
		
		user = Users.get_by_id(user_id)
		if user:
			user_ptr = user.key
			channel_id = int(channel_id)
			channel = Channels.get_by_id(channel_id)
			thread_id = int(thread_id)
			thread = Threads.get_by_id(thread_id)
			comment_id = int(comment_id)
			comment = ThreadDiscussions.get_by_id(comment_id)
			if channel and thread and comment:
				channel_ptr = channel.key
				thread_ptr = thread.key
				is_admin = Channel_Admins.query(Channel_Admins.channel_ptr == channel_ptr, Channel_Admins.user_ptr == user_ptr, Channel_Admins.isDeleted == 0).count()
				if is_admin == 1 or comment.user_ptr == user_ptr:				
					comment.isDeleted = 1
					comment.put()

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
