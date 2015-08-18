import webapp2
import json
import logging
from datetime import datetime, timedelta
from service._users.sessions import BaseHandler, LoginRequired
from handlers.push import push_dict
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, DEFAULT_ANON_IMG_URL
from db.database import Users, Channels, Posts, Channel_Admins, Views, Channel_Followers, DBUserGCMId
from google.appengine.api import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.ext import ndb

class PostsHandler(BaseHandler,webapp2.RequestHandler):
	"""docstring for Posts"""
	# Request URL - /channels/:channel_id/posts POST
	# Request Params - user_id, channel_id(generated), text, post_img, post_by (user or channel)
	# Response - status, post:(  post_id(generated),
	#							 text, img_url, 
	#							 time, first_name, last_name, 
	#							 user_img_url, user_branch)
	# if curated_bit is not set, status = 200
	
	@LoginRequired
	def post(self,channel_id):

		isAnonymous = self.request.get('isAnonymous').strip() #fetching True/False
		user_id = self.request.get('user_id').strip()
		post_by = self.request.get('post_by').strip()
		text = self.request.get('text').strip()
		image = self.request.get('post_img')
		if image!='':
			image = images.Image(image)
			# Transform the image
			image.resize(width=400, height=400)
			image = image.execute_transforms(output_encoding=images.JPEG)
			size = len(image)
			if size > 1000000:
				self.response.set_status(400,"Image too big")
				return
		query = Users.query(Users.user_id == user_id).fetch()
		if len(query) == 1:
			user = query[0]
			user_ptr = user.key
			first_name = user.first_name
			last_name = user.last_name
			user_img_url = user_ptr.urlsafe()
			branch = user.branch
			
			channel_id = int(channel_id)
			channel = Channels.get_by_id(channel_id)
			if channel:
				channel_ptr = channel.key
				db = Posts()
				admin_query = Channel_Admins.query(Channel_Admins.channel_ptr == channel_ptr, Channel_Admins.user_ptr == user_ptr).fetch()    #  if the person posting is admin, pending bit should be 0
				if len(admin_query) == 1:
					db.pending_bit = 0
				db.text = text
				if image != '':
					db.img = image
				else:
					db.img = ''

				db.channel_ptr = channel_ptr
				db.user_ptr = user_ptr
				db.isAnonymous = isAnonymous
				db.post_by = post_by
				k = db.put()
				post_items = k.get()
				text = post_items.text
				
				created_time = date_to_string(utc_to_ist(post_items.created_time))

				#TODO isAnonymous to be checked
				_dict = {}
				
				if isAnonymous == 'True':
					_dict['full_name'] = 'Anonymous'
					_dict['img_url'] = DEFAULT_ANON_IMG_URL
				else:
					if post_by == 'user':
						_dict['full_name'] = first_name + ' ' + last_name
						_dict['branch'] = branch
						_dict['img_url'] = DEFAULT_ROOT_IMG_URL + str(user_img_url)
					else:
						_dict['full_name'] = channel.channel_name
						_dict['img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.key.urlsafe())
				_dict['post_by'] = post_by
				
				_dict['post_id'] = k.id()
				_dict['text'] = text
				_dict['pending_bit'] = post_items.pending_bit
				if image != '':
					_dict['post_img_url'] = DEFAULT_ROOT_IMG_URL + str(k.urlsafe())
				else:
					_dict['post_img_url'] = ''

				_dict['created_time'] = created_time
				user.last_seen = datetime.now()
				user.put()

				#-----------------------Send Notifs-------------------------------
				result = Channel_Followers.query(Channel_Followers.getNotification == 1, Channel_Followers.channel_ptr == channel_ptr)
				notify_these_users = result.fetch()

				
				for user in notify_these_users:
					user_ptr = user.user_ptr
					user_gcm_id = DBUserGCMId.query(DBUserGCMId.user_ptr == user_ptr).fetch()
					gcm_id = user_gcm_id[0].gcm_id
					push_dict(gcm_id, _dict)

				
					
				#-----------------------------------------------------------
				
				self.response.set_status(200, 'Awesome')
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
				user_id = int(self.userid)
				user = Users.get_by_id(user_id)
		#		posts_query = Posts.query(ndb.OR(ndb.AND(Posts.channel_ptr == channel.key, Posts.pending_bit == 0), ndb.AND(Posts.channel_ptr == channel.key, Posts.user_ptr == user.key, Posts.pending_bit == 1)))
				if user.type_ == 'admin' or user.type_ == 'superuser':
					is_admin = Channel_Admins.query(Channel_Admins.channel_ptr == channel.key, Channel_Admins.user_ptr == user.key).fetch()
					posts_query = Posts.query(Posts.channel_ptr == channel.key, Posts.isDeleted == 0)
					
				if user.type_ == 'user':
					posts_query = Posts.query(ndb.OR(ndb.AND(Posts.channel_ptr == channel.key, Posts.pending_bit == 0, Posts.isDeleted == 0), ndb.AND(Posts.channel_ptr == channel.key, Posts.user_ptr == user.key, Posts.pending_bit == 1, Posts.isDeleted == 0)))
				
				if timestamp:
					lastSeenTime = string_to_date(timestamp) 
					lastSeenTime = ist_to_utc(lastSeenTime)
					posts_query = posts_query.filter(Posts.created_time >= lastSeenTime)

				if limit != -1:
					posts = posts_query.order(-Posts.created_time).fetch(limit,offset=offset)
				else:
					posts = posts_query.order(-Posts.created_time).fetch(offset=offset)

				out = []
				dict_={}
				for post in posts:
					posting_user = Users.get_by_id(post.user_ptr.id())
					has_viewed_query = Views.query(Views.post_ptr == post.key,Views.user_ptr == user.key).fetch()
					num_views_count = Views.query(Views.post_ptr == post.key).count()
					_dict = {}
					_dict['post_id'] = post.key.id()
					_dict['text'] = post.text
					if post.img != '':
						_dict['post_img_url'] = DEFAULT_ROOT_IMG_URL + str(post.key.urlsafe())
					else:
						_dict['post_img_url'] = ''
					if post.isAnonymous == 'True':
						_dict['full_name'] = 'Anonymous'
					else:
						if post.post_by == 'user':
							_dict['full_name'] = posting_user.first_name + ' ' + posting_user.last_name
							_dict['img_url'] = DEFAULT_ROOT_IMG_URL + str(posting_user.key.urlsafe())
							_dict['branch'] = posting_user.branch
						else:
							_dict['full_name'] = channel.channel_name
							_dict['img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.key.urlsafe())
					_dict['post_by'] = post.post_by
					_dict['created_time'] = date_to_string(utc_to_ist(post.created_time))					
					_dict['pending_bit'] = post.pending_bit
					

					if len(has_viewed_query) == 0:
						_dict['num_views'] = num_views_count + 1   #This user is now viewing it
						db = Views()
						db.user_ptr = user.key
						db.post_ptr = post.key
						db.put()	
					else:
						_dict['num_views'] = num_views_count					

					out.append(_dict)

				dict_['posts'] = out
				user.last_seen = datetime.now()
				user.put()
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(404, 'Channel not found')
		else:
			self.response.set_status(400, 'Limit offset standards not followed')

		self.response.write(json.dumps(dict_))
