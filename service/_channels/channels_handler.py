import webapp2
import logging
import json
from db.database import Channels, Users, Channel_Admins
class ChannelsHandler(webapp2.RequestHandler):
		
	# 	Request URL: /channels/:channel_id GET
	# Response : status, description, created_time, admins: array of (first_name,last_name)
	def get(self, channel_id):
		channel = Channels.get_by_id(int(channel_id))
		dict_ = {}
		if channel:
			channel_admins = Channel_Admins.query(Channel_Admins.channel_ptr == channel.key).fetch()
			if len(channel_admins) > 0:
				dict_['description'] = channel.description
				dict_['created_time'] = channel.created_time
				out = []
				for channel_admin in channel_admins:
					admin = Users.get_by_id(channel_admin.user_ptr.id())
					_dict = {}
					_dict['first_name'] = admin.first_name
					_dict['last_name'] = admin.last_name
					out.append(_dict)
				dict_['admins'] = out
				self.response.set_status(200, 'Awesome')
			else:
				self.response.set_status(400, 'No admins of the channel! Weird!')
		else:
			self.response.set_status(404, 'Channel not found')

		self.response.write(json.dumps(dict_))

	def put(self, channel_id):

		db = Channels.get_by_id(int(channel_id))
		logging.info(db.pending_bit)
		if db.pending_bit == 1:
			db.pending_bit = 0
		logging.info(db.pending_bit)
		db.put()