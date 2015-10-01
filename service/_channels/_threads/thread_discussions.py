import webapp2
import json
import logging
from datetime import datetime, timedelta
from service._users.sessions import BaseHandler, LoginRequired
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, DEFAULT_ANON_IMG_URL
from db.database import *
from google.appengine.ext import ndb

class ThreadDiscussionsHandler(BaseHandler,webapp2.RequestHandler):
	"""docstring for Threads"""
	# Request URL - /channels/:channel_id/threads/:thread_id/discussions POST
	# Request Params - channel_id(generated), topic
	# Response - status
	# if curated_bit is not set, status = 200
	
	@LoginRequired
	def post(self,channel_id, thread_id):

		user_id = self.userid
		user_id = int(user_id)
		data = json.loads(self.request.body)
		text = data.get('text').strip()
		dict_ = {}
		
		user = Users.get_by_id(user_id)
		if user:
			user_ptr = user.key
			thread_id = int(thread_id)
			thread = Threads.get_by_id(thread_id)
			channel_id = int(channel_id)
			channel = Channels.get_by_id(channel_id)
			if thread and channel:
				thread_ptr = thread.key
				channel_ptr = channel.key
				is_following = Channel_Followers.query(Channel_Followers.channel_ptr == channel_ptr, Channel_Followers.user_ptr == user_ptr, Channel_Followers.isDeleted == 0).count()
				if is_following == 1:				
					db = ThreadDiscussions()
					
					db.text = text
					db.thread_ptr = thread_ptr
					db.user_ptr = user_ptr
					k = db.put()
					comment = k.get()
					posting_user = comment.user_ptr.get()

					_dict = {}
					_dict['comment_id'] = comment.key.id()
					_dict['text'] = comment.text
			
					_dict['full_name'] = posting_user.first_name + ' ' + posting_user.last_name
					_dict['branch'] = posting_user.branch
				
					_dict['added_time'] = date_to_string(utc_to_ist(comment.added_time))

					dict_['comment'] = _dict
					self.response.set_status(200, 'Awesome')
				else:
					logging.error('Not allowed')
					self.response.set_status(401, 'Not allowed')
				#-----------------------------------------------------------	
			else:
				logging.error('Invalid channel')
				self.response.set_status(401, 'Invalid channel')
		else:
			self.response.set_status(401, 'Invalid user')

		self.response.write(json.dumps(dict_))

	# 	Request URL: /channels/:channel_id/threads/:thread_id/discussions  GET
	# Response: Dictionary of status, posts: array of (post_id(generated),text, img_url, time, user_full_name, user_img_url, user_branch )

	# Query params - limit, offset, timestamp
	@LoginRequired
	def get(self, channel_id, thread_id):
		limit = self.request.get('limit')
		offset = self.request.get('offset')
		timestamp = self.request.get('timestamp')
		dict_ = {}
		user_id = self.userid
		user_id = int(user_id)
		if limit and offset:
			limit = int(limit)
			offset= int(offset)
			thread = Threads.get_by_id(int(thread_id))

			if thread:

				user = Users.get_by_id(user_id)
				
				thread_discussions_query = ThreadDiscussions.query(ndb.AND(ThreadDiscussions.thread_ptr == thread.key, ThreadDiscussions.isDeleted == 0))
				
				if timestamp:
					lastSeenTime = string_to_date(timestamp) 
					lastSeenTime = ist_to_utc(lastSeenTime)
					thread_discussions_query = posts_query.filter(Threads.added_time >= lastSeenTime)

				if limit != -1:
					threadDiscussions = thread_discussions_query.order(ThreadDiscussions.added_time).fetch(limit,offset=offset)
				else:
					threadDiscussions = thread_discussions_query.order(ThreadDiscussions.added_time).fetch(offset=offset)

				out = []
				dict_={}
				for comment in threadDiscussions:
					posting_user = comment.user_ptr.get()

					_dict = {}
					_dict['comment_id'] = comment.key.id()
					_dict['text'] = comment.text
			
					_dict['full_name'] = posting_user.first_name + ' ' + posting_user.last_name
					_dict['branch'] = posting_user.branch
				
					_dict['added_time'] = date_to_string(utc_to_ist(comment.added_time))					
	
					out.append(_dict)

				dict_['threadDiscussions'] = out
				# user.last_seen = datetime.now()
				# user.put()

				has_viewed_query = ThreadViews.query(ThreadViews.thread_ptr == thread.key,ThreadViews.user_ptr == user.key).fetch()

				if len(has_viewed_query) == 0:
					db1 = ThreadViews()
					db1.thread_ptr = thread.key
					db1.user_ptr = user.key
					db1.put()
				
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(404, 'Channel not found')
		else:
			self.response.set_status(400, 'Limit offset standards not followed')

		self.response.write(json.dumps(dict_))
