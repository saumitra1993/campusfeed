import logging
import webapp2
from google.appengine.ext import ndb
from datetime import datetime, timedelta
from service._channels._posts.posts import PostsHandler
from db.database import *
import json
from service._users.sessions import BaseHandler, LoginRequired
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, DEFAULT_ANON_IMG_URL, POST_LIMIT
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date

class UserFeed(BaseHandler, webapp2.RequestHandler):
	"""docstring for UserFeed"""
	
	# RequestURL: /users/:user_id/feed GET
	# Response: user_id -> key -> 
	#			channels from channel_followers (=> channel keys) -> 
	#			key.get() (=> channels) -> 
	#			channel_ptr posts order by time
	# dict:{
	#  		'feed':[
	#             	{
	#            	  'channel_name':
	#              	  'channel_posts': [{},{}.....{}]
	#             	},
	#               {
	#                 'channel_name':
	#                 'channel_posts': [{},{}.....{}]
	#               }
	#              ]
	#      }
	@LoginRequired
	def get(self,user_id):

		limit = int(self.request.get('limit'))
		offset = int(self.request.get('offset'))
		timestamp = self.request.get('timestamp')
		u_id = int(self.userid)
		logging.info(u_id);
		user = Users.get_by_id(u_id)
		result = Channel_Followers.query(Channel_Followers.user_ptr == user.key)
		
		if limit != -1:
			user_followed_channels = result.fetch(limit,offset=offset)
		else:
			user_followed_channels = result.fetch(offset=offset)
		
		
		dict_ = {}
		channel_dict = {}
		timestamp = user.last_seen
		if timestamp is None:
			timestamp = datetime.now() - timedelta(days=2000)	
		for user_followed_channel in user_followed_channels:	
			# posts_handler = PostsHandler()
			# posts_of_channel = posts_handler.get(channel_ptr.id())
			# logging.warn(posts_of_channel)
			channel_details = user_followed_channel.channel_ptr.get()
			channel_ptr = user_followed_channel.channel_ptr
			admin_bool = 0
			if user.type_ == 'admin' or user.type_ == 'superuser':
				is_admin = Channel_Admins.query(Channel_Admins.channel_ptr == channel_ptr, Channel_Admins.user_ptr == user.key).fetch()
				posts_query = Posts.query(Posts.channel_ptr == channel_ptr, Posts.isDeleted == 0)
				if len(is_admin) == 1:
					admin_bool = 1

			if user.type_ == 'user':
				posts_query = Posts.query(ndb.OR(ndb.AND(Posts.channel_ptr == channel_ptr, Posts.pending_bit == 0, Posts.isDeleted == 0), ndb.AND(Posts.channel_ptr == channel_ptr, Posts.user_ptr == user.key, Posts.pending_bit == 1, Posts.isDeleted == 0)))
			
			posts_query_filtered = posts_query.filter(Posts.created_time >= timestamp)
			posts_query_filtered_count = posts_query_filtered.count()
			if posts_query_filtered_count > POST_LIMIT:
				posts = posts_query_filtered.order(-Posts.created_time).fetch(POST_LIMIT)
				
			elif posts_query_filtered_count == 0:
				posts = posts_query.order(-Posts.created_time).fetch(POST_LIMIT)		
				
			else:
				posts = posts_query_filtered.order(-Posts.created_time).fetch()

			logging.info(channel_details)
			logging.info(posts)
			out = []
			for channel_post in posts:
				posting_user = channel_post.user_ptr.get()
				has_viewed_query = Views.query(Views.post_ptr == channel_post.key,Views.user_ptr == user.key).fetch()
				num_views_count = Views.query(Views.post_ptr == channel_post.key).count()
				_dict_channel_posts = {}
				_dict_channel_posts['channel_name'] = channel_details.channel_name
				_dict_channel_posts['channel_tag'] = channel_details.tag
				if channel_details.img != '':
					_dict_channel_posts['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel_details.key.urlsafe())
				else:
					_dict_channel_posts['channel_img_url'] = DEFAULT_IMG_URL
				_dict_channel_posts['is_admin'] = admin_bool
				_dict_channel_posts['channel_id'] = channel_details.key.id()
				_dict_channel_posts['post_id'] = channel_post.key.id()
				_dict_channel_posts['text'] = channel_post.text
				if channel_post.img != '':
					_dict_channel_posts['post_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel_post.key.urlsafe())
				else:
					_dict_channel_posts['post_img_url'] = ''

				if channel_post.isAnonymous == 'True':
					_dict_channel_posts['full_name'] = 'Anonymous'
					_dict_channel_posts['img_url'] = DEFAULT_ANON_IMG_URL
				else:
					if channel_post.post_by == 'user':
						_dict_channel_posts['full_name'] = posting_user.first_name + ' ' + posting_user.last_name
						if posting_user.img != '':
							_dict_channel_posts['img_url'] = DEFAULT_ROOT_IMG_URL+ str(posting_user.key.urlsafe())
						else:
							_dict_channel_posts['img_url'] = DEFAULT_IMG_URL
						_dict_channel_posts['branch'] = posting_user.branch
					else:
						_dict_channel_posts['full_name'] = channel_details.channel_name
						if channel_details.img != '':
							_dict_channel_posts['img_url'] = DEFAULT_ROOT_IMG_URL + str(channel_details.key.urlsafe())
						else:
							_dict_channel_posts['img_url'] = DEFAULT_IMG_URL
				_dict_channel_posts['post_by'] = channel_post.post_by
				_dict_channel_posts['created_time'] = date_to_string(utc_to_ist(channel_post.created_time))					
				_dict_channel_posts['pending_bit'] = channel_post.pending_bit
				if len(has_viewed_query) == 0:
					_dict_channel_posts['num_views'] = num_views_count + 1   #This user is now viewing it
					db = Views()
					db.user_ptr = user.key
					db.post_ptr = channel_post.key
					db.put()	
				else:
					_dict_channel_posts['num_views'] = num_views_count

				out.append(_dict_channel_posts)
			
			channel_dict[channel_details.key.id()] = out

		dict_['channel_posts'] = channel_dict
		self.response.set_status(200, 'Awesome')
		user.last_seen = datetime.now()
		user.put()
		self.response.write(json.dumps(dict_))