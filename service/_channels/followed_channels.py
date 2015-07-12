import webapp2
import logging
import json
import datetime
from google.appengine.ext import ndb
from service._users.sessions import BaseHandler
from db.database import Channels, Users, Channel_Followers
from const.constants import DEFAULT_ROOT_URL, DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL

class FollowedChannels(BaseHandler, webapp2.RequestHandler):
	"""docstring for GetMyChannels"""
	# Request URL- /users/:user_id/channels GET
	# Response - Dictionary of status(200/400), 
	# user_channels: array of (   channel_id, 
	#                       channel_name, 
	#                   channel_img_url, num_followers)
	# Query params-
	# limit and offset  
	def get(self,user_id):
		limit = self.request.get('limit')
		offset = self.request.get('offset')
		dict_ = {}
		if limit and offset:
			logging.info("%s %s"%(limit, offset))
			user_query = Users.query(Users.user_id == user_id)
			user = user_query.fetch()
			logging.info(user)
			limit = int(limit)
			offset= int(offset)
			if len(user) == 1:
				qry = Channel_Followers.query(Channel_Followers.user_ptr == user[0].key)
				if limit!=-1:
					followed_channels = qry.fetch(limit,offset= offset)
					
				else:
					followed_channels = qry.fetch(offset= offset)
					
				logging.info(followed_channels)
				out=[]
				for followed_channel in followed_channels:
					channel = Channels.get_by_id(followed_channel.channel_ptr.id())
					logging.info(channel)
					_dict = {}
					_dict['channel_id'] = followed_channel.channel_ptr.id()
					_dict['channel_name'] = channel.channel_name
					_dict['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == followed_channel.channel_ptr).count()
					
					if channel.channel_img_url:
						_dict['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.channel_img_url)
					else:
						_dict['channel_img_url'] = DEFAULT_IMG_URL
					
					logging.info(_dict)
					out.append(_dict)
				dict_['followed_channels'] = out
				self.response.set_status(200, 'Awesome')
				self.session['last-seen'] = datetime.datetime.now()
			else:
				self.response.set_status(401, 'User is malicious. Ask him to go fuck himself.')
		else:
			self.response.set_status(400, 'Limit offset standards are not followed')
		self.response.write(json.dumps(dict_))

	# Request URL: /users/usersid/channels POST
	# Request params: channel_id
	# Response : status
	def post(self, user_id):
		user_query = Users.query(Users.user_id == user_id)
		result = user_query.fetch()

		channel_id = int(self.request.get('channel_id').strip())
		channel_key = ndb.Key('Channels', channel_id)
		
		channel = Channels.get_by_id(channel_key.id())
		
		if len(result) == 1 and channel:
			user = result[0]
			relationship = Channel_Followers.query(Channel_Followers.user_ptr == user.key, Channel_Followers.channel_ptr == channel_key).fetch()
			if len(relationship) == 0:
				db = Channel_Followers()
				db.user_ptr = user.key
				db.channel_ptr = channel_key
				db.put()
				self.response.set_status(200,'Awesome')
				self.session['last-seen'] = datetime.now()
			else:
				self.response.set_status(400,'User id and channel id are related.')
		else:
			self.response.set_status(401,'User or Channel sucks')


		#delete user_id and channel_id from Channel_Followers
		def delete(self, user_id):
			channel_id = int(self.request.get('channel_id').strip())
			channel_ptr = ndb.Key('Channels', channel_id)
			
			user_query = Users.query(Users.user_id == user_id)
			result = user_query.fetch()
			
			if len(result) == 1 :
				user = result[0]
				user_ptr = user.key
				query = Channel_Followers.query(Channel_Followers.user_ptr == user_ptr, Channel_Followers.channel_ptr == channel_ptr).fetch()
				if len(query) == 1:
					user_channel = query[0]
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
					self.response.set_status(401,'Duplicate user_ptr-channel_ptr combo!!!')
			else:
				self.response.set_status(401,'Channel Follower cannot be deleted as User can\'t be fetched.')
