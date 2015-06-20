import webapp2
import json
import logging
import datetime
from service._users.sessions import BaseHandler
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID
from db.database import Users, Channels, Posts
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb

class PostsHandler(blobstore_handlers.BlobstoreUploadHandler, BaseHandler):
	"""docstring for Posts"""
	# Request URL - /channels/:channel_id/posts POST
	# Request Params - user_id, channel_id(generated), text, img
	# Response - status, post:(  post_id(generated),
	#							 text, img_url, 
	#							 time, first_name, last_name, 
	#							 user_img_url, user_branch)
	# if curated_bit is not set, status = 200
	# else status = 911
	
	def post(self,channel_id):

		logging.info(self.request)

		user_id = self.request.get('user_id').strip()
		query = Users.query(Users.user_id == user_id).fetch()
		user_ptr = query[0].key
		first_name = query[0].first_name
		last_name = query[0].last_name
		user_img_url = query[0].user_img_url
		branch = query[0].branch
		
		channel_id = int(channel_id)
		result = Channels.get_by_id(channel_id)
		curated_bit = result.curated_bit
		channel_ptr = result.key

		db = Posts()
		db.text = self.request.get('text').strip()
		try:
			db.post_img_url = self.get_uploads('post_img_url')[0].key()
		except:
			db.post_img_url = blobstore.BlobKey(DEFAULT_IMG_ID)
		db.channel_ptr = channel_ptr
		db.user_ptr = user_ptr
		k=db.put()
		post_items = k.get()
		post_key = post_items.key
		text = post_items.text
		post_img_url = post_items.post_img_url
		time = date_to_string(post_items.time)

		
		_dict = {}
		if curated_bit:
			logging.info("Rukk ja bhai tu ,please _/\_")
			_dict['status'] = 911
		else:
			_dict['first_name'] = first_name
			_dict['last_name'] = last_name
			_dict['user_img_url'] = DEFAULT_ROOT_IMG_URL + str(user_img_url)
			_dict['branch'] = branch
			_dict['post_id'] = post_key.id()
			_dict['text'] = text
			_dict['post_img_url'] = DEFAULT_ROOT_IMG_URL + str(post_img_url)
			_dict['time'] = time
			self.response.set_status(200, 'Awesome')

		self.response.write(json.dumps(_dict))

	# 	Request URL: /channels/:channel_id/posts GET
	# Response: Dictionary of status, posts: array of (post_id(generated),text, img_url, time, user_full_name, user_img_url, user_branch )

	# Query params - limit, offset, timestamp
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
				user_id = self.session['userid']
				user = Users.get_by_id(user_id)
				posts_query = Posts.query(ndb.OR(ndb.AND(Posts.channel_ptr == channel.key, Posts.pending_bit == 0), ndb.AND(Posts.channel_ptr == channel.key, Posts.user_ptr == user.key, Posts.pending_bit == 1)))
				
				if timestamp:
					lastSeenTime = string_to_date(timestamp) 
					lastSeenTime = ist_to_utc(lastSeenTime)
					posts_query = posts_query.filter(Posts.time >= lastSeenTime)

				if limit != -1:
					posts = posts_query.fetch(limit,offset=offset)
				else:
					posts = posts_query.fetch(offset=offset)

				out = []

				for post in posts:
					posting_user = Users.get_by_id(post.user_ptr.id())
					_dict = {}
					_dict['post_id'] = post.key.id()
					_dict['text'] = post.text
					_dict['img_url'] = DEFAULT_ROOT_IMG_URL + str(post.post_img_url)
					_dict['time'] = date_to_string(utc_to_ist(post.time))
					_dict['user_full_name'] = posting_user.first_name+' '+posting_user.last_name
					_dict['user_img_url'] = posting_user.user_img_url
					_dict['branch'] = posting_user.branch
					_dict['pending_bit'] = post.pending_bit
					out.append(_dict)

				dict_['posts'] = out
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(404, 'Channel not found')
		else:
			self.response.set_status(400, 'Limit offset standards not followed')

		self.response.write(json.dumps(dict_))
