import webapp2
import json
import logging
from datetime import datetime, timedelta
from service._users.sessions import BaseHandler, LoginRequired
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, DEFAULT_ANON_IMG_URL
from db.database import *
from google.appengine.ext import ndb

class ThreadsHandler(BaseHandler,webapp2.RequestHandler):
	"""docstring for Threads"""
	# Request URL - /channels/:channel_id/threads POST
	# Request Params - channel_id(generated), topic
	# Response - status
	# if curated_bit is not set, status = 200
	
	@LoginRequired
	def post(self,channel_id):

		user_id = self.userid
		user_id = int(user_id)
		topic = self.request.get('topic').strip()
		_dict = {}
		
		user = Users.get_by_id(user_id)
		if user:
			user_ptr = user.key
			channel_id = int(channel_id)
			channel = Channels.get_by_id(channel_id)
			if channel:
				channel_ptr = channel.key
				is_following = Channel_Followers.query(Channel_Followers.channel_ptr == channel_ptr, Channel_Followers.user_ptr == user_ptr, Channel_Followers.isDeleted == 0).count()
				if is_following == 1:				
					db = Threads()
					
					db.topic = topic
					db.channel_ptr = channel_ptr
					db.started_by_user_ptr = user_ptr
					k = db.put()
					self.response.set_status(200, 'Awesome')
				else:
					self.response.set_status(401, 'Invalid channel')
				#-----------------------------------------------------------	
			else:
				self.response.set_status(401, 'Invalid channel')
		else:
			self.response.set_status(401, 'Invalid user')

		self.response.write(json.dumps(_dict))

	# 	Request URL: /channels/:channel_id/posts GET
	# Response: Dictionary of status, posts: array of (post_id(generated),text, img_url, time, user_full_name, user_img_url, user_branch )

	# Query params - limit, offset, timestamp
	@LoginRequired
	def get(self, channel_id):
		limit = self.request.get('limit')
		offset = self.request.get('offset')
		timestamp = self.request.get('timestamp')
		dict_ = {}
		if limit and offset:
			limit = int(limit)
			offset= int(offset)
			channel = Channels.get_by_id(int(channel_id))

			if channel:

				user = Users.get_by_id(user_id)
				
				threads_query = Threads.query(ndb.AND(Threads.channel_ptr == channel.key, Threads.isDeleted == 0))
				
				if timestamp:
					lastSeenTime = string_to_date(timestamp) 
					lastSeenTime = ist_to_utc(lastSeenTime)
					threads_query = posts_query.filter(Threads.created_time >= lastSeenTime)

				if limit != -1:
					threads = threads_query.order(-Threads.created_time).fetch(limit,offset=offset)
				else:
					threads = threads_query.order(-Threads.created_time).fetch(offset=offset)

				out = []
				dict_={}
				for thread in threads:
					posting_user = thread.started_by_user_ptr.get()
					num_views_count = ThreadViews.query(ThreadViews.thread_ptr == post.key).count()
					_dict = {}
					_dict['thread_id'] = thread.key.id()
					_dict['topic'] = thread.topic
			
					_dict['full_name'] = posting_user.first_name + ' ' + posting_user.last_name
					_dict['branch'] = posting_user.branch
				
					_dict['created_time'] = date_to_string(utc_to_ist(post.created_time))					
	
					_dict['num_views'] = num_views_count					

					out.append(_dict)

				dict_['threads'] = out
				# user.last_seen = datetime.now()
				# user.put()

				
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(404, 'Channel not found')
		else:
			self.response.set_status(400, 'Limit offset standards not followed')

		self.response.write(json.dumps(dict_))
