import webapp2
import logging
import json
from operator import itemgetter
from datetime import datetime, timedelta
from google.appengine.ext import ndb
from service._users.sessions import BaseHandler, LoginRequired
from db.database import Channels, Users, Channel_Followers, Channel_Admins, Posts
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_ROOT_URL, DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, tags

class FollowedChannels(BaseHandler, webapp2.RequestHandler):
	"""docstring for GetMyChannels"""
	# Request URL- /users/:user_id/channels GET
	# Response - Dictionary of status(200/400), 
	# user_channels: array of (   channel_id, 
	#                       channel_name, 
	#                   channel_img_url, num_followers)
	# Query params-
	# limit and offset 
	@LoginRequired
	def get(self,user_id):
		limit = self.request.get('limit')
		offset = self.request.get('offset')
		timestamp = self.request.get('timestamp')
		requested_tag = self.request.get('tag')
		_dict = {}
		if limit and offset and requested_tag:
			limit = int(limit)
			offset= int(offset)
			user_id = int(self.userid)
			user = Users.get_by_id(user_id)
			dict1 = {}
			timestamp1 = user.last_seen
			for tag in tags:
				dict1[tag] = []

			if requested_tag == 'all':
				followed_channels_query = Channel_Followers.query(Channel_Followers.isDeleted == 0,Channel_Followers.user_ptr == user.key).fetch()
				for followed_channel in followed_channels_query:
					channel = followed_channel.channel_ptr.get()
					if channel.pending_bit == 0:
						dict_ = {}
						dict_['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.isDeleted == 0).count()
						dict_['channel_id'] = channel.key.id()
						dict_['channel_name'] = channel.channel_name
						dict_['pending_bit'] = 0
						dict_['channel_tag'] = channel.tag
						dict_['description'] = channel.description
						dict_['is_admin'] = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.channel_ptr == channel.key, Channel_Admins.isDeleted == 0).count()
						posts_query = Posts.query(ndb.AND(Posts.channel_ptr == channel.key, Posts.pending_bit == 0, Posts.isDeleted == 0, Posts.created_time >= timestamp1))
					
						post_count = posts_query.count()
						dict_['new_post_count'] = post_count
						if channel.img != '':
							dict_['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.key.urlsafe())
						else:
							dict_['channel_img_url'] = DEFAULT_IMG_URL

						dict1[channel.tag].append(dict_)

				for tag in tags:
					dict1[tag] = sorted(dict1[tag], key=itemgetter('num_followers'), reverse=True)

				_dict['followed_channels'] = dict1
			elif requested_tag in tags:
				channels_qry = Channels.query(Channels.isDeleted == 0,Channels.pending_bit == 0,Channels.tag == requested_tag).order(-Channels.created_time)
				if timestamp:
					lastSeenTime = string_to_date(timestamp) 
					lastSeenTime = ist_to_utc(lastSeenTime)
					channels_qry = channels_qry.filter(Channels.created_time >= lastSeenTime)
				
				channels = channels_qry.fetch(offset= offset)
				
				out = []
				i = 0
				limit = limit - offset
				for channel in channels:
					if i < limit:
						dict_ = {}
						is_following = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.user_ptr == user.key,Channel_Followers.isDeleted == 0).count()
						if is_following == 1:
							dict_['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.isDeleted == 0).count()
							dict_['channel_id'] = channel.key.id()
							dict_['channel_name'] = channel.channel_name
							dict_['pending_bit'] = 0
							dict_['channel_tag'] = channel.tag
							dict_['description'] = channel.description
							dict_['is_admin'] = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.channel_ptr == channel.key, Channel_Admins.isDeleted == 0).count()
							posts_query = Posts.query(ndb.AND(Posts.channel_ptr == channel.key, Posts.pending_bit == 0, Posts.isDeleted == 0))
						
							posts_query = posts_query.filter(Posts.created_time >= timestamp1)
							post_count = posts_query.count()
							dict_['new_post_count'] = post_count
							if channel.img != '':
								dict_['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.key.urlsafe())
							else:
								dict_['channel_img_url'] = DEFAULT_IMG_URL
							out.append(dict_)
							i = i + 1
					else:
						break

				out = sorted(out, key=itemgetter('num_followers'), reverse=True)
				dict1[requested_tag] = out
				_dict['followed_channels'] = dict1
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(400, 'Tag standards are not followed')
		else:
			self.response.set_status(400, 'Limit offset standards are not followed')
		self.response.write(json.dumps(_dict))



	# Request URL: /users/usersid/channels POST
	# Request params: channel_id
	# Response : status
	def post(self, user_id):
		user_id = int(user_id)
		user = Users.get_by_id(user_id)
		data = json.loads(self.request.body)
		channel_id = int(data.get('channel_id').strip())
		getNotification = int(data.get('get_notification'))
		
		channel = Channels.get_by_id(channel_id)
		
		if user and channel:
			new_relationship = Channel_Followers.query(Channel_Followers.user_ptr == user.key, Channel_Followers.channel_ptr == channel.key).fetch()
			if len(new_relationship) == 0:
				db = Channel_Followers()
				db.user_ptr = user.key
				db.channel_ptr = channel.key
				db.getNotification = getNotification
				db.put()
				self.response.set_status(200,'Awesome')
			elif len(new_relationship) == 1:
				rel = new_relationship[0]
				rel.isDeleted=0;
				rel.put()
			else:
				self.response.set_status(400,'User id and channel id are related.')
		else:
			self.response.set_status(401,'User or Channel sucks')
		self.response.write("Blah")


	#delete user_id and channel_id from Channel_Followers
	def delete(self, user_id):
		logging.info("Here")
		data = json.loads(self.request.body)
		channel_id = int(data.get('channel_id').strip())
		channel_ptr = ndb.Key('Channels', channel_id)
		user_id = int(user_id)
		user = Users.get_by_id(user_id)
		if user:
			user_ptr = user.key
			query = Channel_Followers.query(Channel_Followers.user_ptr == user_ptr, Channel_Followers.channel_ptr == channel_ptr).fetch()
			if len(query) == 1:
				user_channel = query[0]
				logging.info(user_channel)
				key = user_channel.key
				if key:
				#   key.delete()    
					db = Channel_Followers.get_by_id(int(key.id()))
					if db.isDeleted == 0:
						db.isDeleted = 1
						db.put()
						self.response.set_status(200,'Awesome.Entry deleted.')
				else:
					self.response.set_status(400,'Unable to fetch key.')
			else:
				self.response.set_status(401,'Duplicate or none user_ptr-channel_ptr combo!!!')
		else:
			self.response.set_status(401,'Channel Follower cannot be deleted as User can\'t be fetched.')
