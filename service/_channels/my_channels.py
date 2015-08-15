import webapp2
import json
import logging
from datetime import datetime, timedelta
from service._users.sessions import BaseHandler
from db.database import Users, Channel_Admins, Channels, Channel_Followers
from const.functions import utc_to_ist, ist_to_utc, date_to_string, string_to_date
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID

class MyChannels(BaseHandler, webapp2.RequestHandler):
	
	# Request URL: /users/userid/mychannels GET
	# Response : Dictionary of status, all_channels: array of (channel_id, channel_name, channel_img_url, num_folllowers)
	def get(self, user_id):
		limit = self.request.get('limit')
		offset = self.request.get('offset')
		user_id = str(user_id)
		logging.info(user_id)
		dict_ = {}
		out = []
		if limit and offset:
			limit = int(limit)
			offset= int(offset)
			user_query = Users.query(Users.user_id == user_id)
			result = user_query.fetch()
			if len(result) == 1:
				user = result[0]
				if user.type_ == 'admin' or user.type_ == 'superuser':
					channel_admins_qry = Channel_Admins.query(Channel_Admins.user_ptr == user.key, Channel_Admins.isDeleted == 0)
					if limit!=-1:
						channel_admins = channel_admins_qry.fetch(limit,offset= offset)
					else:
						channel_admins = channel_admins_qry.fetch(offset= offset)

					
					for channel_admin in channel_admins:
						channel = Channels.get_by_id(channel_admin.channel_ptr.id())
						_dict = {}
						_dict['channel_id'] = channel.key.id()
						_dict['channel_name'] = channel.channel_name
						_dict['channel_tag'] = channel.tag
						_dict['num_followers'] = Channel_Followers.query(Channel_Followers.channel_ptr == channel.key, Channel_Followers.isDeleted == 0).count()
						_dict['pending_bit'] = channel.pending_bit
						if channel.img != '':
							_dict['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(channel.key.urlsafe())
						else:
							_dict['channel_img_url'] = DEFAULT_IMG_URL
						
						logging.info(_dict)
						out.append(_dict)
						
				dict_['my_channels'] = out
				self.response.set_status(200, 'Awesome')
					
			else:
				logging.info("or here")
				self.response.set_status(401, 'User is malicious. Ask him to go fuck himself.')
		else:
			self.response.set_status(400, 'Limit offset standards are not followed')
		self.response.write(json.dumps(dict_))
