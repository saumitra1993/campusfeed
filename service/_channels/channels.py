import webapp2
import json
import logging
from datetime import datetime, timedelta
from google.appengine.api import blobstore
from service._users.sessions import BaseHandler, LoginRequired
from db.database import Users, Channel_Admins, Channels, Channel_Followers, Posts
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import images
from google.appengine.ext import ndb
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID, tags
from operator import itemgetter

class AllChannels(BaseHandler,webapp2.RequestHandler):
	"""docstring for Channels"""
	# Request URL - /channels POST
	# Request params - user_id, channel_name, channel_img_url, description, isAnonymous
	# Response - status
	@LoginRequired
	def post(self):

		user_id = self.request.get('user_id').strip()
		user_id = int(user_id)
		isAnonymous = self.request.get('isAnonymous')
		channel_name = self.request.get('channel_name').strip()
		descr = self.request.get('description').strip()
		user = Users.get_by_id(user_id)    #query will store entire 'list' of db cols
		image = self.request.get('channel_img')
		tag = self.request.get('tag')
		logging.info(channel_name)
		logging.info(descr)
		logging.info(isAnonymous)
		logging.info(user_id)
		if image!='':
			image = images.Image(image)
			# Transform the image
			image.resize(width=200, height=200)
			image = image.execute_transforms(output_encoding=images.JPEG)
			size = len(image)
			if size > 1000000:
				self.response.set_status(400,"Image too big")
				return
		
		if user:
			#if user.type_ == 'superuser':
			
			user_key = user.key
			check_channel_name_query = Channels.query(ndb.OR(Channels.channel_name == channel_name, Channels.channel_name == channel_name.upper(), Channels.channel_name == channel_name.title())).fetch()  #Channel name can be either all caps or first letter caps, rest small. .title() function converts string into the latter format
			if len(check_channel_name_query) == 0:

				db = Channels()
				db.channel_name = channel_name
				db.description = descr
				
				#when a new channel is created, user type cannot already be 'admin'
				if user.type_ == 'user':
					user.type_ = 'admin'   #updating 'user' to 'admin
					user.put()
				elif user.type_ == 'superuser':
					db.pending_bit = 0
				
				if image != '':
					db.img = image
				else:
					db.img = ''
				db.tag = tag
				channel_key = db.put()

				db1 = Channel_Admins()
				db1.user_ptr = user_key
				db1.channel_ptr = channel_key
				db1.isAnonymous = isAnonymous
				k1 = db1.put()

				#if 'superuser' is creating a channel that means it's approved, 
				#therefore make them follow their channel.
				#for 'admin', superusers ll approve their channel first and
				#then make them follow their channel. 
				if user.type_ == 'superuser':
					db2 = Channel_Followers()
					db2.user_ptr = user_key
					db2.channel_ptr = channel_key
					db2.put()
				logging.info('...Inserted into DB user with key... %s ' % k1)

				user.last_seen = datetime.now()
				user.put()
			else:
				self.response.set_status(400,'Channel name already exists')
			
			# else:
			# 	self.response.set_status(401,'Unauthorized')

		else:
			self.response.set_status(401,'Invalid user')



	# Request URL - /channels GET

	# Response - Dictionary of status, all_channels: array of (channel_id, channel_name, channel_img_url, num_folllowers)

	# Query params-
	# limit and offset
	@LoginRequired
	def get(self):
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
			if requested_tag == 'all':
				for tag in tags:
					channels_qry = Channels.query(Channels.isDeleted == 0,Channels.pending_bit == 0,Channels.tag == tag).order(-Channels.created_time)
					if timestamp:
						lastSeenTime = string_to_date(timestamp) 
						lastSeenTime = ist_to_utc(lastSeenTime)
						channels_qry = channels_qry.filter(Channels.created_time >= lastSeenTime)
					
					channels = channels_qry.fetch(offset= offset)
					logging.info(channels)
					out = []
					i = 0
					limit = limit - offset
					for channel in channels:
						if i < limit:
							dict_ = {}
							is_following = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.user_ptr == user.key,Channel_Followers.isDeleted == 0).count()
							if is_following == 0:
								dict_['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.isDeleted == 0).count()
								dict_['channel_id'] = channel.key.id()
								dict_['channel_name'] = channel.channel_name
								dict_['pending_bit'] = 0
								dict_['channel_tag'] = channel.tag
								dict_['description'] = channel.description
								dict_['is_admin'] = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.channel_ptr == channel.key, Channel_Admins.isDeleted == 0).count()
								
								if channel.img != '':
									dict_['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.key.urlsafe())
								else:
									dict_['channel_img_url'] = DEFAULT_IMG_URL
								out.append(dict_)
								i = i + 1
						else:
							break

					out = sorted(out, key=itemgetter('num_followers'), reverse=True)
					dict1[tag] = out

				user.last_seen = datetime.now()
				user.put()
				_dict['all_channels'] = dict1
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
						if is_following == 0:
							dict_['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.isDeleted == 0).count()
							dict_['channel_id'] = channel.key.id()
							dict_['channel_name'] = channel.channel_name
							dict_['pending_bit'] = 0
							dict_['channel_tag'] = channel.tag
							dict_['description'] = channel.description
							dict_['is_admin'] = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.channel_ptr == channel.key, Channel_Admins.isDeleted == 0).count()
							
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
				_dict['all_channels'] = dict1
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(400, 'Tag standards are not followed')
		else:
			self.response.set_status(400, 'Limit offset standards are not followed')
		self.response.write(json.dumps(_dict))