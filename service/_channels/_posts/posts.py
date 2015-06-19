import webapp2
import json
import logging
import datetime
from service._users.sessions import BaseHandler
from db.database import Users, Channels, Posts
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class PostsHandler(blobstore_handlers.BlobstoreUploadHandler):
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
		query = Users.query().filter(Users.user_id == user_id).fetch()
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
		db.post_img_url = self.get_uploads('post_img_url')[0].key()
		db.channel_ptr = channel_ptr
		db.user_ptr = user_ptr
		k=db.put()
		post_items = k.get()
		post_key = post_items.key
		text = post_items.text
		post_img_url = post_items.post_img_url
		time = post_items.time.strftime("%B %d, %Y %H:%M:%S")

		
		_dict = {}
		if curated_bit:
			logging.info("Rukk ja bhai tu ,please _/\_")
			_dict['status'] = 911
		else:
			_dict['status'] = 200
			_dict['first_name'] = first_name
			_dict['last_name'] = last_name
			_dict['user_img_url'] = "http://localhost:9080/pic/" + str(user_img_url)
			_dict['branch'] = branch
			_dict['post_id'] = post_key.id()
			_dict['text'] = text
			_dict['post_img_url'] = "http://localhost:9080/pic/" + str(post_img_url)
			_dict['time'] = time
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
			user_id = self.session['userid']
			user = Users.get_by_id(user_id)
			posts_query = Posts.query(ndb.OR(ndb.AND(Posts.channel_ptr == channel.key, Posts.pending_bit == 0), ndb.AND(Posts.channel_ptr == channel.key, Posts.user_ptr == user.key, Posts.pending_bit == 1)))
			
		elif limit and offset and timestamp:
			timestamp = time.strptime(timestamp,'%d %m %Y %H:%M:%S')

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
			_dict['img_url'] = post.img_url
			_dict['time'] = post.time
			_dict['user_full_name'] = posting_user.first_name+' '+posting_user.last_name
			_dict['user_img_url'] = posting_user.user_img_url
			_dict['branch'] = posting_user.branch
			out.append(_dict)
		dict_['posts'] = out
