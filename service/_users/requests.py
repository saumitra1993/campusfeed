import webapp2
import json
import logging
from datetime import datetime
from service._users.sessions import BaseHandler
from db.database import Users, Channel_Admins, Channels, Channel_Followers
from const.constants import DEFAULT_IMG_URL, DEFAULT_ROOT_IMG_URL, DEFAULT_IMG_ID

class PendingChannels(BaseHandler,webapp2.RequestHandler):
	
		def get(self, user_id):
			limit = self.request.get('limit')
			offset = self.request.get('offset')
			dict_ = {}
			if limit and offset:
				limit = int(limit)
				offset = int(offset)
				user_id = int(user_id)
				user = Users.get_by_id(user_id)
				if user:
					if user.type_ == 'superuser':
						pending_channels_qry = Channels.query(Channels.pending_bit == 1)
						if limit!=-1:
							pending_channels = pending_channels_qry.fetch(limit,offset= offset)
						else:
							pending_channels = pending_channels_qry.fetch(offset= offset)

						out = []
						for pending_channel in pending_channels:
							_dict = {}
							_dict['channel_id'] = pending_channel.key.id()
							_dict['channel_name'] = pending_channel.channel_name
							_dict['num_followers'] = 0
							if pending_channel.img != '':
								_dict['channel_img_url'] = DEFAULT_ROOT_IMG_URL + str(pending_channel.key.urlsafe())
							else:
								_dict['channel_img_url'] = DEFAULT_IMG_URL
							
							logging.info(_dict)
							out.append(_dict)
						dict_['pending_channels'] = out
						self.response.set_status(200, 'Awesome')
						self.session['last-seen'] = datetime.now()
					else:
						self.response.set_status(401, 'User is malicious. Ask him to go fuck himself.')
				else:
					self.response.set_status(401, 'User is malicious. Ask him to go fuck himself.')
			else:
				self.response.set_status(400, 'Limit offset standards are not followed')
			
			self.response.write(json.dumps(dict_))

				# elif user.type == 'admin':
				# 	user_channels = Channel_Admins.query(Channel_Admins.user_ptr == user.key).fetch()
					

				# 	for channel in user_channels:
				# 		pending_posts_qry = Posts.query(Posts.channel_ptr == channel.key, Posts.pending_bit == 1)

				# 		if limitp!=-1:
				# 			pending_posts = pending_channels_qry.fetch(limitp,offset= offsetp)
				# 		else:
				# 			pending_posts = pending_channels_qry.fetch(offset= offsetp)
				# 		_dict = {}
				# 		channel_ptr = pending_post.channel_ptr
				# 		channel = Channels.get_by_id(channel_ptr.id())
				# 		_dict['channels'] = channel.channel_name
