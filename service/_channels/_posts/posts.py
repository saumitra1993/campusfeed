import webapp2
import json
import logging
from datetime import datetime, timedelta
from service._users.sessions import BaseHandler, LoginRequired
from handlers.push import push_dict
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import TaskRetryOptions
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, DEFAULT_ANON_IMG_URL, DEFAULT_ROOT_FILE_URL, DEFAULT_ROOT_URL
from db.database import Users, Channels, Posts, Channel_Admins, Views, Channel_Followers, DBUserGCMId, DBProxyUserGCMId, PostFiles, DBPhoneNumbers
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url

class PostsHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
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

		post_by = self.request.get('post_by').strip()
		text = self.request.get('text')
		logging.info(text)
		user_id = self.request.get('user_id')
		logging.info(user_id);
		user_id = int(user_id)
		# image = self.get_uploads('post_img')[0]

		# _dict = {}
		# if image!='':
			
		# 	size = len(image)
		# 	logging.info(size)
			
		# 	image = images.Image(image)
		# 	# Transform the image
		# 	image.resize(width=800, height=800)
		# 	image = image.execute_transforms(output_encoding=images.JPEG)
			
		# 	size = len(image)
		# 	logging.info("After resize %s"%size)
		# 	if size > 900000:
		# 		self.response.set_status(400,"Image too big")
		# 		return
		user = Users.get_by_id(user_id)
		if user:
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
				admin_query = Channel_Admins.query(Channel_Admins.channel_ptr == channel_ptr, Channel_Admins.user_ptr == user_ptr, Channel_Admins.isDeleted == 0).count()    #  if the person posting is admin, pending bit should be 0
				if admin_query == 1:
					db.pending_bit = 0
				db.text = text
				# if image != '':
				# 	db.img = image
				# else:
				# 	db.img = ''
				db.img = ''
				db.channel_ptr = channel_ptr
				db.user_ptr = user_ptr
				db.isAnonymous = isAnonymous
				db.post_by = post_by
				k = db.put()
				try:
					files = self.get_uploads('file')
					for attached_file in files:
						db1 = PostFiles()
						db1.post_ptr = k
						db1.file_key = attached_file.key()
						db1.put()
				finally:
					logging.info("No files")

				post_items = k.get()
				text = post_items.text
				
				created_time = date_to_string(utc_to_ist(post_items.created_time))

				
				_dict = {}
				
				_dict['text'] =  (text[:75] + '..') if len(text) > 75 else text
				_dict['channel_name'] = channel.channel_name
				_dict['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.isDeleted == 0).count()
				_dict['channel_id'] = channel.key.id()
				if channel.img != '':
					_dict['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.key.urlsafe())
				else:
					_dict['channel_img_url'] = DEFAULT_IMG_URL
				_dict['is_admin'] = admin_query
				user.last_seen = datetime.now()
				user.put()

				retry_limit = 0
				eta = None
				#-----------------------Send Notifs-------------------------------
				taskqueue.add(
					url = '/tasks/pushmsg',
					params = {
						'message' : json.dumps(_dict),
						'channel_id' : channel.key.id(),
						'user_id':user_ptr.id(),
					},
					name = str(k.id()),
					queue_name = "PUSH-MESSAGE",
					retry_options = TaskRetryOptions(
						task_retry_limit=retry_limit,
						min_backoff_seconds = 120,
						max_backoff_seconds = 120,
					),
					eta = eta
				)

				# if channel.channel_name == 'AXIS\'15':
				# 	logging.info("Sending proxy phone this text..")
				# 	message = {}
				# 	factor = 1
				# 	message['message'] = text 
				# 	num_chars = len(text)
				# 	if num_chars > 145:
				# 		factor = int(num_chars/145) + 1

				# 	logging.info("Number of characters in text are %s", num_chars)

				# 	users = Users.query(Users.user_id == "14098").fetch()
					
				# 	user = users[0]
				# 	user_ids = DBProxyUserGCMId.query(DBProxyUserGCMId.user_ptr == user.key).fetch()
				# 	numbers = DBPhoneNumbers.query().fetch()
				# 	outn = []
				# 	for number_obj in numbers:
				# 		outn.append(number_obj.number)

				# 	for user_id in user_ids:
				# 		if len(outn) > 0:
				# 			count =  user_id.message_count + len(outn)*factor
				# 			if count < 100:
				# 				user_id.message_count = count
				# 				user_id.put()
				# 				message['numbers'] = outn
				# 				outn = []
				# 				push_dict(user_id.gcm_id, message)
				# 			elif 100 - user_id.message_count < len(outn)*factor:
				# 				j = 0
				# 				out = []
				# 				while j < (100 - user_id.message_count)/factor:
				# 					out.append(outn.pop())
				# 					j = j + 1

				# 				if len(out) > 0:
				# 					user_id.message_count = 100
				# 					user_id.put()
				# 					message['numbers'] = out
				# 					push_dict(user_id.gcm_id, message)
				# 			else:
				# 				logging.error("ALL phones exhausted!")
				# 		else:
				# 			break

				
				user_channel = Channel_Followers.query(Channel_Followers.channel_ptr == channel_ptr, Channel_Followers.user_ptr == user_ptr).fetch()
				if len(user_channel) == 1:
					user_channel[0].last_seen = datetime.now()
					user_channel[0].put()
					
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
				logging.info(user_id)
				if user_id == -1:
					user = Users()
					user.type_ = 'user'
				else:
					user = Users.get_by_id(user_id)			

		#		posts_query = Posts.query(ndb.OR(ndb.AND(Posts.channel_ptr == channel.key, Posts.pending_bit == 0), ndb.AND(Posts.channel_ptr == channel.key, Posts.user_ptr == user.key, Posts.pending_bit == 1)))
				if user.type_ == 'admin' or user.type_ == 'superuser':
					is_admin = Channel_Admins.query(Channel_Admins.channel_ptr == channel.key, Channel_Admins.user_ptr == user.key).fetch()
					posts_query = Posts.query(Posts.channel_ptr == channel.key, Posts.isDeleted == 0)
					
				if user.type_ == 'user':
					posts_query = Posts.query(ndb.AND(Posts.channel_ptr == channel.key, Posts.pending_bit == 0, Posts.isDeleted == 0))
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
					if user_id != -1:
						has_viewed_query = Views.query(Views.post_ptr == post.key,Views.user_ptr == user.key).fetch()
					else:
						has_viewed_query = ['a']   #any random thing with one element

					num_views_count = Views.query(Views.post_ptr == post.key).count()
					_dict = {}
					_dict['post_id'] = post.key.id()
					_dict['text'] = post.text

					
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
					
					post_files = PostFiles.query(PostFiles.post_ptr == post.key).fetch()

					out2 = []
					out3 = []
					for post_file in post_files:
						dict2 = {}
						file_key = post_file.file_key
						blob_info= blobstore.BlobInfo.get(file_key)
						file_name = blob_info.filename
						dict2['filename'] = file_name
						if 'jpg' in file_name or 'JPG' in file_name or 'png' in file_name or 'PNG' in file_name or 'jpeg' in file_name or 'JPEG' in file_name or 'gif' in file_name:
							dict2['url'] = get_serving_url(file_key)
							out3.append(dict2)
						else:
							dict2['url'] = DEFAULT_ROOT_FILE_URL + str(file_key)
							out2.append(dict2)

					_dict['files'] = out2
					_dict['images'] = out3

					if post.img != '':
						_dict['post_img_url'] = DEFAULT_ROOT_IMG_URL + str(post.key.urlsafe())
					elif len(out3) > 0:
						_dict['post_img_url'] = DEFAULT_ROOT_URL + 'images/old_app_image.png'
					else:
						_dict['post_img_url'] = ''

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
				# user.last_seen = datetime.now()
				# user.put()

				try:
					user_channel = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.user_ptr == user.key).fetch()
					if len(user_channel) == 1:
						user_channel[0].last_seen = datetime.now()
						user_channel[0].put()
				finally:
					self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(404, 'Channel not found')
		else:
			self.response.set_status(400, 'Limit offset standards not followed')

		self.response.write(json.dumps(dict_))
