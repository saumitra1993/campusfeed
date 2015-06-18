import webapp2
import logging
import json
from const.constants import DEFAULT_ROOT_URL, DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL
from db.database import Channels, Users, Channel_Followers
class GetMyChannels(webapp2.RequestHandler):
	"""docstring for GetMyChannels"""
	# Request URL- /users/:user_id/channels GET
	# Response - Dictionary of status(200/400), 
	# user_channels: array of (   channel_id, 
	# 						channel_name, 
	# 					channel_img_url, num_followers)
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
				dict_['user_channels'] = out
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(401, 'User is malicious. Ask him to go fuck himself.')
		else:
			self.response.set_status(400, 'Limit offset standards are not followed')
		self.response.write(json.dumps(dict_))